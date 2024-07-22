#http://127.0.0.1:5000/database/TexasBit
DATABASE_API_SCHEMA = {
    "openapi": "3.0.0",
    "info": {
        "title": "Local Database API",
        "version": "1.0.0",
        "description": "API for fetching information from a database"
    },
    "servers": [
        {
            "url": "https://api.alfred.fayazk.com"
        }
    ],
    "paths": {
        "/database/{uuid}/{query}": {
            "get": {
                "description": "Get records from database",
                "operationId": "get_records",
                "summary": "Fetch all records for the query",
                "parameters": [
                    {
                        "name": "uuid",
                        "in": "path",
                        "required": True,
                        "description": "The UUID of the project",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "query",
                        "in": "path",
                        "required": True,
                        "description": "only and exact asked question with no details.",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "A response from the database",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "oneOf": [
                                                {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "additionalProperties": True
                                                }
                                                },
                                                {
                                                "type": "object",
                                                "additionalProperties": True
                                                }
                                            ]
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Project not found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


