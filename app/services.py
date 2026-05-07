import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Use absolute path for data directory
datafolder = "/app/data"
datasource = os.path.join(datafolder, "users.json")

class UserNotFoundError(Exception):
    pass

class DuplicateEmailError(Exception):
    pass

class ValidationError(Exception):
    pass

def check_dataset_exists():
    if not os.path.exists(datafolder):
        os.mkdir(datafolder)
    if not os.path.exists(datasource):
        with open(datasource, "w") as f:
            f.write(json.dumps({"data": [], "next_id": 1}, indent=2))
            
def read_usersdata() -> Dict:
    check_dataset_exists()
    with open(datasource, "r") as f:
        content = f.read()
        if content == "":
            content = '{"data": [], "next_id": 1}'
        users = json.loads(content)
    return users

def write_usersdata(data: Dict) -> None:
    check_dataset_exists()
    with open(datasource, "w") as f:
        json.dumps(data, indent=2)
        f.write(json.dumps(data, indent=2))

def add_userdata(user: dict) -> Dict:
    """Add user and return user with ID"""
    users = read_usersdata()
    
    # Check for duplicate email
    for existing_user in users["data"]:
        if existing_user.get("email") == user.get("email"):
            raise DuplicateEmailError(f"Email {user['email']} already exists")
    
    user_id = users["next_id"]
    user["id"] = user_id
    users["data"].append(user)
    users["next_id"] = user_id + 1
    
    write_usersdata(users)
    return user

def get_user_by_id(user_id: int) -> Dict:
    """Get user by ID"""
    users = read_usersdata()
    for user in users["data"]:
        if user.get("id") == user_id:
            return user
    raise UserNotFoundError(f"User with ID {user_id} not found")

def update_user(user_id: int, user_data: dict) -> Dict:
    """Update user by ID"""
    users = read_usersdata()
    
    user_index = None
    for idx, user in enumerate(users["data"]):
        if user.get("id") == user_id:
            user_index = idx
            break
    
    if user_index is None:
        raise UserNotFoundError(f"User with ID {user_id} not found")
    
    # Check for duplicate email (if email is being changed)
    if "email" in user_data:
        for idx, user in enumerate(users["data"]):
            if idx != user_index and user.get("email") == user_data["email"]:
                raise DuplicateEmailError(f"Email {user_data['email']} already exists")
    
    users["data"][user_index].update(user_data)
    write_usersdata(users)
    return users["data"][user_index]

def delete_user(user_id: int) -> bool:
    """Delete user by ID"""
    users = read_usersdata()
    
    user_index = None
    for idx, user in enumerate(users["data"]):
        if user.get("id") == user_id:
            user_index = idx
            break
    
    if user_index is None:
        raise UserNotFoundError(f"User with ID {user_id} not found")
    
    del users["data"][user_index]
    write_usersdata(users)
    return True

def get_all_users() -> List[Dict]:
    """Get all users"""
    users = read_usersdata()
    return users["data"]

def get_total_users() -> int:
    """Get total user count"""
    return len(get_all_users())
