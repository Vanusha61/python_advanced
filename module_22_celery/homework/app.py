"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, jsonify, request
from celery import Celery, group
from tasks import blur_image_task, celery, r
import os


app = Flask(__name__)


@app.route("/blur", methods=["POST"])
def blur():
    images = request.files.getlist("image")
    list_images = []
    if images:
        count_image = 1
        dir_name = 'uploads'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for image in images:
            image.save(os.path.join(dir_name, f"blur_{count_image}.png"))
            list_images.append(os.path.join(dir_name, f"blur_{count_image}.png"))
            count_image += 1
        task_group = group(
            blur_image_task.s(image) for image in list_images
        )
        # Запускаем группу задач и сохраняем её
        result = task_group.apply_async()
        result.save()

        return jsonify({"group_id": result.id}), 202
    return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<string:group_id>', methods=["GET"])
def status(group_id):
    result = celery.GroupResult.restore(group_id)
    if result:
        res = {}
        res["progress"] = f"{result.completed_count()}/{len(result)}"
        res["status"] = "SUCCESS" if result.ready() else "PROCESSING"
        res["pending"] = len(result) - result.completed_count()
        return jsonify({"status": res}), 200
    return jsonify({'error': 'Group not found'}), 404




@app.route('/subscribe', methods=["POST"])
def subscribe():
    email = request.json.get("email")
    if email:
        r.sadd('email_subscribers', email)
        return jsonify({"email": email}), 201
    return jsonify({'error': 'Email not found'}), 400

@app.route('/unsubscribe', methods=["POST"])
def unsubscribe():
    email = request.json.get("email")
    if email:
        r.srem('email_subscribers', email)
        return jsonify({"result":"Удален"}), 201
    return jsonify({'error': 'Email not found'}), 400