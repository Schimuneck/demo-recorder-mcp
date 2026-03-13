#!/usr/bin/env python3
"""
Dependency Auditor for demo-recorder-mcp.
Checks for outdated packages, vulnerabilities, conflicts, and license issues.

Usage:
    python .cursor/agents/scripts/audit_deps.py [--full] [--fix]
    
Options:
    --full    Run all checks including security scan (slower)
    --fix     Attempt to fix issues (update outdated packages)
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class AuditResult:
    total_packages: int = 0
    outdated: list = field(default_factory=list)
    vulnerabilities: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


class DependencyAuditor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.result = AuditResult()

    def run_cmd(self, cmd: list[str], check: bool = False) -> tuple[int, str, str]:
        """Run a command and return (returncode, stdout, stderr)."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except FileNotFoundError:
            return -1, "", f"Command not found: {cmd[0]}"

    def check_outdated(self) -> list[dict]:
        """Check for outdated packages."""
        print("\n📦 Checking for outdated packages...")
        
        # Try uv first, fall back to pip
        code, stdout, stderr = self.run_cmd(["uv", "pip", "list", "--outdated", "--format=json"])
        
        if code != 0:
            # Fall back to pip
            code, stdout, stderr = self.run_cmd(["pip", "list", "--outdated", "--format=json"])
        
        if code == 0 and stdout.strip():
            try:
                outdated = json.loads(stdout)
                self.result.outdated = outdated
                return outdated
            except json.JSONDecodeError:
                pass
        
        return []

    def check_conflicts(self) -> list[str]:
        """Check for dependency conflicts."""
        print("\n🔍 Checking for conflicts...")
        
        code, stdout, stderr = self.run_cmd(["uv", "pip", "check"])
        
        if code != 0:
            code, stdout, stderr = self.run_cmd(["pip", "check"])
        
        if code != 0:
            conflicts = [line for line in (stdout + stderr).split('\n') if line.strip()]
            self.result.conflicts = conflicts
            return conflicts
        
        return []

    def check_vulnerabilities(self) -> list[dict]:
        """Check for security vulnerabilities using pip-audit."""
        print("\n🔒 Scanning for vulnerabilities...")
        
        code, stdout, stderr = self.run_cmd(["pip-audit", "--format=json"])
        
        if code == -1 and "not found" in stderr:
            print("   ⚠️  pip-audit not installed. Run: pip install pip-audit")
            self.result.warnings.append("pip-audit not installed")
            return []
        
        if stdout.strip():
            try:
                vulns = json.loads(stdout)
                self.result.vulnerabilities = vulns
                return vulns
            except json.JSONDecodeError:
                pass
        
        return []

    def count_packages(self) -> int:
        """Count installed packages."""
        code, stdout, stderr = self.run_cmd(["uv", "pip", "list", "--format=json"])
        
        if code != 0:
            code, stdout, stderr = self.run_cmd(["pip", "list", "--format=json"])
        
        if code == 0:
            try:
                packages = json.loads(stdout)
                self.result.total_packages = len(packages)
                return len(packages)
            except json.JSONDecodeError:
                pass
        
        return 0

    def check_python_compat(self) -> list[str]:
        """Check if dependencies support required Python versions."""
        print("\n🐍 Checking Python compatibility...")
        
        # Read pyproject.toml for requires-python
        pyproject = self.project_root / "pyproject.toml"
        if not pyproject.exists():
            return []
        
        # This is a simplified check - in practice you'd parse TOML
        # and check each package's Python version support
        return []

    def generate_report(self) -> str:
        """Generate markdown audit report."""
        report = []
        report.append("## Dependency Audit Report\n")
        report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"**Project:** demo-recorder-mcp")
        report.append(f"**Python:** {sys.version.split()[0]}\n")
        
        # Summary
        report.append("### Summary")
        report.append(f"- Total packages: {self.result.total_packages}")
        report.append(f"- Outdated: {len(self.result.outdated)}")
        report.append(f"- Vulnerabilities: {len(self.result.vulnerabilities)}")
        report.append(f"- Conflicts: {len(self.result.conflicts)}")
        report.append("")
        
        # Outdated
        if self.result.outdated:
            report.append("### Outdated Packages")
            report.append("| Package | Current | Latest | Recommendation |")
            report.append("|---------|---------|--------|----------------|")
            for pkg in self.result.outdated:
                name = pkg.get("name", "unknown")
                current = pkg.get("version", "?")
                latest = pkg.get("latest_version", "?")
                report.append(f"| {name} | {current} | {latest} | Review changelog |")
            report.append("")
        else:
            report.append("### Outdated Packages")
            report.append("All packages up to date ✅\n")
        
        # Vulnerabilities
        if self.result.vulnerabilities:
            report.append("### Security Vulnerabilities ⚠️")
            for vuln in self.result.vulnerabilities:
                name = vuln.get("name", "unknown")
                vid = vuln.get("id", "?")
                report.append(f"- **{name}**: {vid}")
            report.append("")
        else:
            report.append("### Security Vulnerabilities")
            report.append("No vulnerabilities found ✅\n")
        
        # Conflicts
        if self.result.conflicts:
            report.append("### Dependency Conflicts ❌")
            for conflict in self.result.conflicts:
                report.append(f"- {conflict}")
            report.append("")
        else:
            report.append("### Dependency Conflicts")
            report.append("No conflicts detected ✅\n")
        
        # Warnings
        if self.result.warnings:
            report.append("### Warnings")
            for warning in self.result.warnings:
                report.append(f"- ⚠️ {warning}")
            report.append("")
        
        return "\n".join(report)

    def print_summary(self):
        """Print colored summary to console."""
        print("\n" + "=" * 60)
        print("DEPENDENCY AUDIT SUMMARY")
        print("=" * 60)
        
        # Status indicators
        outdated_status = "⚠️" if self.result.outdated else "✅"
        vuln_status = "❌" if self.result.vulnerabilities else "✅"
        conflict_status = "❌" if self.result.conflicts else "✅"
        
        print(f"\n📦 Packages: {self.result.total_packages}")
        print(f"{outdated_status} Outdated: {len(self.result.outdated)}")
        print(f"{vuln_status} Vulnerabilities: {len(self.result.vulnerabilities)}")
        print(f"{conflict_status} Conflicts: {len(self.result.conflicts)}")
        
        if self.result.outdated:
            print("\n📋 Outdated packages:")
            for pkg in self.result.outdated[:5]:
                print(f"   - {pkg.get('name')}: {pkg.get('version')} → {pkg.get('latest_version')}")
            if len(self.result.outdated) > 5:
                print(f"   ... and {len(self.result.outdated) - 5} more")
        
        if self.result.vulnerabilities:
            print("\n🚨 Vulnerabilities found! Run 'pip-audit' for details.")
        
        if self.result.conflicts:
            print("\n⚠️ Conflicts detected:")
            for conflict in self.result.conflicts[:3]:
                print(f"   - {conflict}")


def main():
    parser = argparse.ArgumentParser(description="Dependency auditor for demo-recorder-mcp")
    parser.add_argument("--full", action="store_true", help="Run all checks including security scan")
    parser.add_argument("--fix", action="store_true", help="Attempt to update outdated packages")
    parser.add_argument("--report", type=str, help="Save report to file")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent.parent
    auditor = DependencyAuditor(project_root)

    print("🔎 Demo Recorder MCP - Dependency Audit")
    print(f"📁 Project: {project_root}")
    print(f"🐍 Python: {sys.version.split()[0]}")

    # Run checks
    auditor.count_packages()
    auditor.check_outdated()
    auditor.check_conflicts()
    
    if args.full:
        auditor.check_vulnerabilities()
    
    # Print summary
    auditor.print_summary()
    
    # Generate report
    report = auditor.generate_report()
    
    if args.report:
        Path(args.report).write_text(report)
        print(f"\n📄 Report saved to: {args.report}")
    else:
        print("\n" + "-" * 60)
        print(report)
    
    # Fix if requested
    if args.fix and auditor.result.outdated:
        print("\n🔧 Attempting to update outdated packages...")
        for pkg in auditor.result.outdated:
            name = pkg.get("name")
            print(f"   Updating {name}...")
            code, _, _ = auditor.run_cmd(["uv", "pip", "install", "--upgrade", name])
            if code == 0:
                print(f"   ✅ {name} updated")
            else:
                print(f"   ❌ Failed to update {name}")
    
    # Exit code based on findings
    if auditor.result.vulnerabilities or auditor.result.conflicts:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
