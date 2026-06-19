from flask import Flask, redirect, render_template, request, url_for

from services.catalog_service import load_catalog
from services.post_service import create_post, get_posts
from services.match_service import get_ranked_matches


app = Flask(__name__)


@app.route("/")
def index():
    posts = get_posts()
    return render_template("index.html", posts=posts)


@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    catalog = load_catalog()

    if request.method == "POST":
        post = create_post(request.form, catalog)
        return redirect(url_for("post_detail", post_id=post["id"]))

    return render_template("new_post.html", catalog=catalog)


@app.route("/posts/<post_id>")
def post_detail(post_id):
    posts = get_posts()
    post = next((item for item in posts if item["id"] == post_id), None)
    if post is None:
        return redirect(url_for("index"))

    matches = get_ranked_matches(post, posts)
    return render_template("post_detail.html", post=post, matches=matches)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
