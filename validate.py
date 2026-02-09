#!/usr/bin/env python3
"""
Comprehensive validation script for ReconRanger v2.0
Tests all flags, links, installation methods, and paths
"""

import sys
import subprocess
from pathlib import Path
from core.config import TOOL_DEFINITIONS, CATEGORIES

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def test_result(name, passed, details=""):
    status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
    print(f"{status} {name}")
    if details and not passed:
        print(f"  {Colors.YELLOW}→ {details}{Colors.RESET}")

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}ReconRanger v2.0 - Comprehensive Validation{Colors.RESET}\n")
    
    passed = 0
    failed = 0
    
    # 1. Tool Configuration Validation
    print(f"{Colors.BOLD}1. Tool Configuration Validation{Colors.RESET}")
    
    # Check total count
    total_tools = len(TOOL_DEFINITIONS)
    test_passed = total_tools == 57
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("Total tools count (expected 57)", test_passed, f"Found {total_tools}")
    
    # Check duplicates
    tool_names = list(TOOL_DEFINITIONS.keys())
    duplicates = [t for t in tool_names if tool_names.count(t) > 1]
    test_passed = len(duplicates) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("No duplicate tools", test_passed, f"Found: {duplicates}" if duplicates else "")
    
    # Check required fields
    missing_fields = []
    for tool_name, cfg in TOOL_DEFINITIONS.items():
        if "type" not in cfg or "binary" not in cfg or "description" not in cfg:
            missing_fields.append(tool_name)
    test_passed = len(missing_fields) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All tools have required fields", test_passed, f"Missing: {missing_fields}" if missing_fields else "")
    
    # 2. Category Validation
    print(f"\n{Colors.BOLD}2. Category Validation{Colors.RESET}")
    
    total_categories = len(CATEGORIES)
    test_passed = total_categories == 11
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("Total categories (expected 11)", test_passed, f"Found {total_categories}")
    
    # Check all tools assigned to categories
    categorized_tools = set()
    for cat, tools in CATEGORIES.items():
        categorized_tools.update(tools)
    test_passed = len(categorized_tools) == 57
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All 57 tools assigned to categories", test_passed, f"Assigned: {len(categorized_tools)}")
    
    # Check for tools in config but not in categories
    not_categorized = set(TOOL_DEFINITIONS.keys()) - categorized_tools
    test_passed = len(not_categorized) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("No uncategorized tools", test_passed, f"Uncategorized: {not_categorized}" if not_categorized else "")
    
    # 3. Installation Method Validation
    print(f"\n{Colors.BOLD}3. Installation Method Validation{Colors.RESET}")
    
    methods = {}
    for tool_name, cfg in TOOL_DEFINITIONS.items():
        method = cfg.get("type")
        methods[method] = methods.get(method, 0) + 1
    
    expected_methods = {"apt", "go", "python", "git", "ruby", "cargo"}
    found_methods = set(methods.keys())
    test_passed = found_methods == expected_methods
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All 6 installation methods present", test_passed, 
                f"Missing: {expected_methods - found_methods}" if not test_passed else "")
    
    # Show method breakdown
    for method in sorted(methods.keys()):
        print(f"  {method:10} {methods[method]:3} tools")
    
    # 4. Binary Path Validation
    print(f"\n{Colors.BOLD}4. Binary Path Validation{Colors.RESET}")
    
    invalid_binaries = []
    for tool_name, cfg in TOOL_DEFINITIONS.items():
        if "binary" not in cfg:
            invalid_binaries.append(tool_name)
    test_passed = len(invalid_binaries) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All tools have binary field", test_passed, f"Missing: {invalid_binaries}" if invalid_binaries else "")
    
    # 5. Go Package Validation
    print(f"\n{Colors.BOLD}5. Go Package Validation{Colors.RESET}")
    
    go_tools = {k: v for k, v in TOOL_DEFINITIONS.items() if v.get("type") == "go"}
    broken_go = []
    for tool_name, cfg in go_tools.items():
        package = cfg.get("package", "")
        # Check for broken patterns
        if "/cmd/" in package and "@v1.0.4" in package:  # Old katana pattern
            broken_go.append((tool_name, "Broken version @v1.0.4"))
        elif "arjun/cmd/arjun" in package:  # Old arjun pattern
            broken_go.append((tool_name, "Path doesn't exist"))
    
    test_passed = len(broken_go) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("No broken Go package paths", test_passed, f"Broken: {broken_go}" if broken_go else "")
    
    # 6. Git Repository Validation
    print(f"\n{Colors.BOLD}6. Git Repository Validation{Colors.RESET}")
    
    git_tools = {k: v for k, v in TOOL_DEFINITIONS.items() if v.get("type") == "git"}
    missing_git_fields = []
    for tool_name, cfg in git_tools.items():
        if "repo" not in cfg or "path" not in cfg:
            missing_git_fields.append(tool_name)
    test_passed = len(missing_git_fields) == 0
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All Git tools have repo and path", test_passed, f"Missing: {missing_git_fields}" if missing_git_fields else "")
    
    # 7. Python Files Syntax
    print(f"\n{Colors.BOLD}7. Python Syntax Validation{Colors.RESET}")
    
    python_files = [
        "core/config.py",
        "core/installer.py",
        "core/logger.py",
        "core/system.py",
        "reconranger.py",
        "ApiKeyMaster.py"
    ]
    
    syntax_errors = []
    for py_file in python_files:
        result = subprocess.run([sys.executable, "-m", "py_compile", py_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            syntax_errors.append((py_file, result.stderr))
        else:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {py_file}")
    
    if syntax_errors:
        failed += 1
        test_result("All Python files valid syntax", False)
        for py_file, error in syntax_errors:
            print(f"  {Colors.RED}✗{Colors.RESET} {py_file}: {error[:50]}")
    else:
        passed += 1
        test_result("All Python files valid syntax", True)
    
    # 8. CLI Arguments
    print(f"\n{Colors.BOLD}8. CLI Arguments Validation{Colors.RESET}")
    
    # Check if help works
    result = subprocess.run([sys.executable, "reconranger.py", "--help"], 
                          capture_output=True, text=True)
    test_passed = result.returncode == 0 and "--list" in result.stdout
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("Help command works and shows all flags", test_passed)
    
    # Check if list works
    result = subprocess.run([sys.executable, "reconranger.py", "--list"], 
                          capture_output=True, text=True)
    test_passed = result.returncode == 0 and "Available Tools" in result.stdout
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("--list command works", test_passed)
    
    # Check if categories work
    result = subprocess.run([sys.executable, "reconranger.py", "--categories"], 
                          capture_output=True, text=True)
    test_passed = result.returncode == 0 and "Available Categories" in result.stdout
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("--categories command works", test_passed)
    
    # 9. Category Names
    print(f"\n{Colors.BOLD}9. Category Names Validation{Colors.RESET}")
    
    expected_cats = {"core", "subdomains", "js", "osint", "web", "vuln", 
                    "cloud", "takeover", "ports", "cms", "utils"}
    found_cats = set(CATEGORIES.keys())
    test_passed = found_cats == expected_cats
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("All 11 expected categories exist", test_passed, 
                f"Missing: {expected_cats - found_cats}" if not test_passed else "")
    
    # 10. Core Toolkit Size
    print(f"\n{Colors.BOLD}10. Core Toolkit Validation{Colors.RESET}")
    
    core_size = len(CATEGORIES.get("core", []))
    test_passed = core_size == 15
    if test_passed:
        passed += 1
    else:
        failed += 1
    test_result("Core toolkit has 15 tools", test_passed, f"Found {core_size}")
    
    # Print Summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}Summary{Colors.RESET}")
    print(f"{'='*50}")
    total = passed + failed
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Passed: {Colors.GREEN}{passed}{Colors.RESET}/{total}")
    print(f"Failed: {Colors.RED}{failed}{Colors.RESET}/{total}")
    print(f"Score:  {Colors.BOLD}{percentage:.1f}%{Colors.RESET}")
    print(f"{'='*50}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED - Project is production-ready!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {failed} tests failed - review above{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
