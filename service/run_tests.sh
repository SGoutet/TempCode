#!/bin/bash
# Run all tests for the banking service

echo "Running unit tests..."
pytest test/ -v

echo ""
echo "Running API tests with RobotFramework..."
echo "Note: Make sure the API server is running on http://localhost:8000"
robot test/api/auth_tests.robot

