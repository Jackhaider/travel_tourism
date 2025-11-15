# --- compatibility shim for Python 3.14 where pkgutil.get_loader was removed ---
# Flask internally depends on pkgutil.get_loader, which was removed in Python 3.14.
# This provides a safe replacement so Flask can run normally.

import pkgutil
import importlib.util

if not hasattr(pkgutil, 'get_loader'):
    def _compat_get_loader(name):
        # avoid calling find_spec for __main__ (raises ValueError)
        if name == '__main__':
            return None
        try:
            spec = importlib.util.find_spec(name)
        except Exception:
            return None
        return spec.loader if spec else None

    pkgutil.get_loader = _compat_get_loader
# --- end shim ---

from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from models import db, Destination, Booking
from forms import DestinationForm, BookingForm, LoginForm
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Admin login credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

    @app.route('/')
    def index():
        q = request.args.get('q', '')
        if q:
            dests = Destination.query.filter(
                (Destination.name.ilike(f'%{q}%')) |
                (Destination.location.ilike(f'%{q}%'))
            ).all()
        else:
            dests = Destination.query.all()
        return render_template('index.html', destinations=dests, q=q)

    @app.route('/destination/<int:dest_id>')
    def destination(dest_id):
        dest = Destination.query.get_or_404(dest_id)
        form = BookingForm()
        return render_template('destination.html', destination=dest, form=form)

    @app.route('/book/<int:dest_id>', methods=['POST'])
    def book(dest_id):
        dest = Destination.query.get_or_404(dest_id)
        form = BookingForm()

        if form.validate_on_submit():
            booking = Booking(
                destination_id=dest.id,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                num_people=form.num_people.data,
                date=form.date.data
            )
            db.session.add(booking)
            db.session.commit()

            flash('Booking created successfully!', 'success')
            return render_template('booking_success.html',
                                   booking=booking,
                                   destination=dest)

        flash('There was a problem with your booking.', 'danger')
        return render_template('destination.html', destination=dest, form=form)

    # -------------------- ADMIN FUNCTIONS --------------------

    def is_logged_in():
        return session.get('admin_logged_in')

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        form = LoginForm()
        if form.validate_on_submit():
            if (form.username.data == ADMIN_USERNAME and
                    form.password.data == ADMIN_PASSWORD):
                session['admin_logged_in'] = True
                flash('Logged in as admin', 'success')
                return redirect(url_for('admin_dashboard'))

            flash('Invalid credentials!', 'danger')

        return render_template('admin/admin_login.html', form=form)

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        flash('Logged out successfully.', 'info')
        return redirect(url_for('index'))

    @app.route('/admin')
    def admin_dashboard():
        if not is_logged_in():
            return redirect(url_for('admin_login'))
        destinations = Destination.query.all()
        return render_template('admin/admin_dashboard.html',
                               destinations=destinations)

    @app.route('/admin/destination/add', methods=['GET', 'POST'])
    def add_destination():
        if not is_logged_in():
            return redirect(url_for('admin_login'))

        form = DestinationForm()
        if form.validate_on_submit():
            dest = Destination(
                name=form.name.data,
                location=form.location.data,
                price=form.price.data,
                description=form.description.data,
                image=form.image.data
            )
            db.session.add(dest)
            db.session.commit()

            flash('Destination added', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/destination_form.html',
                               form=form, action='Add')

    @app.route('/admin/destination/edit/<int:dest_id>',
               methods=['GET', 'POST'])
    def edit_destination(dest_id):
        if not is_logged_in():
            return redirect(url_for('admin_login'))

        dest = Destination.query.get_or_404(dest_id)
        form = DestinationForm(obj=dest)

        if form.validate_on_submit():
            dest.name = form.name.data
            dest.location = form.location.data
            dest.price = form.price.data
            dest.description = form.description.data
            dest.image = form.image.data

            db.session.commit()

            flash('Destination updated', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/destination_form.html',
                               form=form, action='Edit')

    @app.route('/admin/destination/delete/<int:dest_id>',
               methods=['POST'])
    def delete_destination(dest_id):
        if not is_logged_in():
            return redirect(url_for('admin_login'))

        dest = Destination.query.get_or_404(dest_id)
        db.session.delete(dest)
        db.session.commit()

        flash('Destination deleted', 'info')
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/bookings')
    def admin_bookings():
        if not is_logged_in():
            return redirect(url_for('admin_login'))

        bookings = Booking.query.order_by(
            Booking.created_at.desc()
        ).all()

        return render_template('admin/bookings.html', bookings=bookings)

    @app.route('/admin/booking/cancel/<int:booking_id>',
               methods=['POST'])
    def cancel_booking(booking_id):
        if not is_logged_in():
            return redirect(url_for('admin_login'))

        booking = Booking.query.get_or_404(booking_id)
        booking.status = 'Cancelled'
        db.session.commit()

        flash('Booking cancelled', 'info')
        return redirect(url_for('admin_bookings'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
