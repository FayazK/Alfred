#http://127.0.0.1:5000/database/TexasBit
DATABASE_API_SCHEMA = {
    "openapi": "3.0.0",
    "info": {
        "title": "Local Database API",
        "version": "1.0.0",
        "description": "API for fetching project information from a database"
    },
    "servers": [
        {
            "url": "https://api.alfred.fayazk.com"
        }
    ],
    "paths": {
        "/database/{name}": {
            "get": {
                "description": "Get records for a specific project",
                "operationId": "get_project_records",
                "summary": "Fetch all records for a given project",
                "parameters": [
                    {
                        "name": "name",
                        "in": "path",
                        "required": True,
                        "description": "The name of the project",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "A list of records for the specified project",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "BATT_ID": {
                                                "type": "integer"
                                            },
                                            "Project": {
                                                "type": "string"
                                            },
                                            "Details": {
                                                "type": "string"
                                            },
                                            "MixType": {
                                                "type": "string"
                                            },
                                            "Binder_PG": {
                                                "type": "string"
                                            },
                                            "Binder_Content": {
                                                "type": "number"
                                            },
                                            "NMAS": {
                                                "type": "string"
                                            },
                                            "RAP": {
                                                "type": "number"
                                            },
                                            "Fiber": {
                                                "type": "string"
                                            },
                                            "Dosage": {
                                                "type": "number"
                                            },
                                            "Additive": {
                                                "type": "string"
                                            },
                                            "Dosage1": {
                                                "type": "number"
                                            },
                                            "Specimen_ID": {
                                                "type": "string"
                                            },
                                            "CT_index": {
                                                "type": "number"
                                            }
                                        }
                                    }
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


