responses = {
    401: {
        "description": "Invalid or expired token",
        "content": {
            "application/json": {
                "example": {"detail": "Token not found"}
            }
        }
    },
    403: {
        "description": "No permission",
        "content": {
            "application/json": {
                "example": {"detail": "Insufficient privileges"}
            }
        }
    },
    404: {
        "description": "Item doesn't exist",
        "content": {
            "application/json": {
                "example": {"detail": "Item not found"}
            }
        }
    }
}