def get_simple_task_dict(task):
    """
    Generate a simplified dict of the task for the microcontroller
    :param task: Task MongoEngine obj
    :return: simple_task dict {
        _id: string,
        output_port: [number: int, state: boolean],
        condition: list
    }
    """
    return {
        "_id": str(task["_id"]),
        "output_port": task.output_port.to_mongo().to_dict(),
        "conditions": [
            condition.to_mongo().to_dict() for condition in task.conditions if condition.input_port
        ]
    }
