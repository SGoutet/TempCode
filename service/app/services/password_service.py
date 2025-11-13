"""
Password hashing and verification service using Argon2.
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    """
    Service for password hashing and verification using Argon2 algorithm.
    """
    
    def __init__(self):
        """
        Initialize password hasher with default parameters.
        """
        self.hasher = PasswordHasher()
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using Argon2 algorithm.
        
        Args:
            password: Plain text password to hash.
            
        Returns:
            Hashed password string.
        """
        return self.hasher.hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify.
            password_hash: Hashed password to compare against.
            
        Returns:
            True if password matches, False otherwise.
        """
        try:
            self.hasher.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            return False

