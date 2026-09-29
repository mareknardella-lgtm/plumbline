#!/usr/bin/env python3


def main():
    print("Building Plumbline sandbox runtime image...")
    print("Expected SDK tools not found in path.")
    print("Instructions to build manually:")
    print("1. Use a Python 3.12 base image")
    print("2. pip install pytest pytest-timeout coverage radon ruff freezegun")
    print("3. COPY runtime/plumbline_tools /opt/plumbline_tools")
    print("4. Tag image for reuse")


if __name__ == "__main__":
    main()
