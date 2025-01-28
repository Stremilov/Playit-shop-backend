excel_parser_responses = {
    200: {
        "description": "Успешное получение данных",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "Данные получены",
                        "value": {
                            "status": 200,
                            "details": "Данные получены",
                            "data": {}
                        }
                    },
                }
            }
        }
    },
    400: {
        "description": "Ошибка при получении данных",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_data": {
                        "summary": "Ошибка получения данных",
                        "value": {
                            "status": 400,
                            "detail": "Ошибка при форматировании данных из таблицы"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Ошибка получения данных",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_data": {
                        "summary": "Ошибка получения данных",
                        "value": {
                            "status": 404,
                            "detail": "Такой таблицы не существует"
                        }
                    }
                }
            }
        }
    },
}