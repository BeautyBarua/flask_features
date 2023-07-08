from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    """This route will display all blog posts"""
    # add code here to fetch the job posts from a file

    with open("data.json", "r") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """add a new blog post if a POST request is sent to this route"""
    if request.method == 'POST':
        # Get the form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Read the existing blog posts from the JSON file
        with open("data.json", "r") as file:
            blog_posts = json.load(file)

        # Generate a unique ID for the new blog post
        if blog_posts:
            last_post = blog_posts[-1]
            new_id = last_post['id'] + 1
        else:
            new_id = 1

        # Create a new blog post dictionary
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new blog post to the list
        blog_posts.append(new_post)

        # Save the updated blog posts back to the JSON file
        with open("data.json", "w") as file:
            json.dump(blog_posts, file)

        # Redirect the user back to the home page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """To display the update form"""
    # Fetch the blog posts from the JSON file

    def fetch_post_by_id():
        with open('data.json', 'r') as file:
            blog_posts = json.load(file)
        return blog_posts

    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        updated_post = {
            'id': post_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }

        def update_post_in_file():
            with open('blog_posts.json', 'r+') as file:
                blog_posts = json.load(file)
                for index, post in enumerate(blog_posts):
                    if post['id'] == updated_post['id']:
                        blog_posts[index] = updated_post
                        break
                file.seek(0)  # Move the file pointer to the beginning
                json.dump(blog_posts, file, indent=4)
                file.truncate()  # Clear any remaining content after updating

        update_post_in_file()
        return redirect(url_for('index'))

    # Display the update.html page with the post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000)