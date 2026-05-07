#!/bin/bash

echo "======================================"
echo "COMPREHENSIVE API TESTING"
echo "======================================"
echo ""

echo "1. HEALTH CHECKS"
echo "GET /health"
curl -s http://localhost:8000/health | jq .
echo ""

echo "2. CREATE USER (CRUD - Create)"
echo "POST /users - Valid"
RESPONSE=$(curl -s -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Bob","last_name":"Johnson","email":"bob@example.com","age":35}')
echo "$RESPONSE" | jq .
echo ""

echo "3. GET ALL USERS (CRUD - Read List)"
curl -s http://localhost:8000/users | jq .
echo ""

echo "4. GET USER BY ID (CRUD - Read Single)"
curl -s http://localhost:8000/users/1 | jq .
echo ""

echo "5. UPDATE USER (CRUD - Update)"
curl -s -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Bobby","last_name":"Johnson","email":"bobby@example.com","age":36}' | jq .
echo ""

echo "6. ERROR HANDLING - Duplicate Email"
curl -s -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"bobby@example.com","age":25}' | jq .
echo ""

echo "7. ERROR HANDLING - User Not Found"
curl -s http://localhost:8000/users/999 | jq .
echo ""

echo "8. ERROR HANDLING - Invalid Input (age validation)"
curl -s -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Bad","last_name":"User","email":"bad@example.com","age":200}' | jq .
echo ""

echo "9. DELETE USER (CRUD - Delete)"
curl -s -X DELETE http://localhost:8000/users/1 | jq .
echo ""

echo "10. VERIFY DELETION"
curl -s http://localhost:8000/users | jq .
echo ""

echo "======================================"
echo "API TESTING COMPLETE"
echo "======================================"
