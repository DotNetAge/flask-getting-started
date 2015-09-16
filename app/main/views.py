# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for,current_app,abort
from . import main
from .. import db
from ..models import Post, Comment
from flask.ext.login import login_required, current_user
from .forms import CommentForm, PostForm
from flask_babel import gettext as _


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/')
def index():
    # posts=Post.query.all()

    page_index = request.args.get('page', 1, type=int)

    query = Post.query.order_by(Post.created.desc())

    pagination = query.paginate(page_index, per_page=20, error_out=False)

    posts = pagination.items

    return render_template('index.html',
                           title=_(u'欢迎来到Ray的博客'),
                           posts=posts,
                           pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html', title=u'关于')


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Detail 详情页
    post = Post.query.get_or_404(id)

    # 评论窗体
    form = CommentForm()

    # 保存评论
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post(author=current_user)
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.body.data = post.body

    title = _(u'添加新文章')
    if id > 0:
        title = _(u'编辑 - %(title)', title=post.title)

    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)

@main.route('/shoutdown')
def shutdown():
    if not current_app.testing:
        abort(404)

    shoutdown = request.environ.get('werkzeug.server.shutdown')
    if not shoutdown:
        abort(500)

    shoutdown()
    return u'正在关闭服务端进程...'
