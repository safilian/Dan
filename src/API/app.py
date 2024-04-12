from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
from pathlib import Path

from ACT.src.act import ACTTree


UPLOAD_FOLDER = (
    Path(__file__).parent.parent.parent / "uploads"
)  # Path to the uploads folder
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ACT routes
@app.route("/build-act", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = Path(app.config["UPLOAD_FOLDER"]) / "act" / filename
            file.save(save_path)
            act_tree = ACTTree(save_path)
            return act_tree.root.print_tree()
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    app.run()
