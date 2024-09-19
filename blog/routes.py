from flask import render_template, request, flash, redirect, url_for
from blog import app, db
from blog.forms import EntryForm
from blog.models import Entry


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    return handle_entry(form)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    return handle_entry(form, entry=entry)


def handle_entry(form, entry=None):
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry is None:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
                flash('Post dodany')
            else:
                form.populate_obj(entry)
                flash('Post zaktualizowany')

            db.session.commit()
            return redirect(url_for('index'))
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)
