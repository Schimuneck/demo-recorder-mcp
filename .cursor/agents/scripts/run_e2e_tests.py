#!/usr/bin/env python3
"""
E2E test runner for demo-recorder MCP.
Run after code changes to verify everything works.

Usage:
    python .cursor/agents/scripts/run_e2e_tests.py [--quick] [--container]
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class TestRunner:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def run(self, name: str, cmd: list[str], required: bool = True) -> bool:
        """Run a test command and track result."""
        print(f"\n{'='*60}")
        print(f"TEST: {name}")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"✅ PASSED")
                if result.stdout:
                    print(result.stdout[:500])
                self.results.append((name, "PASSED", None))
                self.passed += 1
                return True
            else:
                print(f"❌ FAILED (exit code {result.returncode})")
                error = result.stderr or result.stdout
                print(error[:500] if error else "No output")
                self.results.append((name, "FAILED", error[:200] if error else None))
                self.failed += 1
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT")
            self.results.append((name, "TIMEOUT", None))
            self.failed += 1
            return False
        except Exception as e:
            print(f"💥 ERROR: {e}")
            self.results.append((name, "ERROR", str(e)))
            self.failed += 1
            return False

    def skip(self, name: str, reason: str):
        """Mark a test as skipped."""
        print(f"\n⏭️  SKIPPED: {name} ({reason})")
        self.results.append((name, "SKIPPED", reason))
        self.skipped += 1

    def report(self):
        """Print final test report."""
        print(f"\n{'='*60}")
        print("E2E TEST REPORT")
        print(f"{'='*60}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Project: {self.project_root}")
        print()
        print(f"Summary: {self.passed} passed, {self.failed} failed, {self.skipped} skipped")
        print()
        
        for name, status, detail in self.results:
            icon = {"PASSED": "✅", "FAILED": "❌", "SKIPPED": "⏭️", "TIMEOUT": "⏰", "ERROR": "💥"}.get(status, "?")
            print(f"  {icon} {name}: {status}")
            if detail and status != "PASSED":
                print(f"      → {detail[:100]}")
        
        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(description="E2E tests for demo-recorder MCP")
    parser.add_argument("--quick", action="store_true", help="Run quick smoke test only")
    parser.add_argument("--container", action="store_true", help="Include container build test")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent.parent
    runner = TestRunner(project_root)

    print(f"Demo Recorder MCP - E2E Test Suite")
    print(f"Project: {project_root}")
    print(f"Mode: {'Quick' if args.quick else 'Full'}")

    # Phase 1: Environment
    runner.run("Python import", [sys.executable, "-c", "import recorder; print('OK')"])
    runner.run("FFmpeg available", ["ffmpeg", "-version"])

    if args.quick:
        # Quick mode: just unit tests
        runner.run("Unit tests", ["uv", "run", "pytest", "tests/", "-v", "-x", "--tb=short"])
        success = runner.report()
        sys.exit(0 if success else 1)

    # Phase 2: Unit tests
    runner.run("Unit tests", ["uv", "run", "pytest", "tests/", "-v", "--tb=short"])

    # Phase 3: Server startup
    runner.run(
        "Server module loads",
        [sys.executable, "-c", "from recorder.server import mcp; print(f'Server: {mcp.name}')"]
    )

    # Phase 4: Tool registration
    runner.run(
        "Tools registered",
        [sys.executable, "-c", """
from recorder.server import mcp
from recorder.backends import get_backend
from recorder.tools import register_all_tools
backend = get_backend()
register_all_tools(mcp, backend)
print(f'Tools registered successfully')
"""]
    )

    # Phase 5: Container build (optional)
    if args.container:
        # Check if podman or docker is available
        podman_check = subprocess.run(["which", "podman"], capture_output=True)
        docker_check = subprocess.run(["which", "docker"], capture_output=True)
        
        if podman_check.returncode == 0:
            runner.run("Container build (podman)", ["podman", "build", "-t", "demo-recorder-mcp:test", "."])
        elif docker_check.returncode == 0:
            runner.run("Container build (docker)", ["docker", "build", "-t", "demo-recorder-mcp:test", "."])
        else:
            runner.skip("Container build", "No container runtime found")
    else:
        runner.skip("Container build", "Use --container to enable")

    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
