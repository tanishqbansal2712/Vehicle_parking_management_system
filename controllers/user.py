from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import db, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


# User Dashboard
@user_bp.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.username == 'admin':
        return redirect(url_for('admin.admin_dashboard'))

    lots = ParkingLot.query.all()
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', lots=lots, reservations=reservations)


# Reserve a Spot (assigns the first available spot)
@user_bp.route('/reserve/<int:lot_id>', methods=['POST'])
@login_required
def reserve_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    # Get first available spot
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        flash("No available spots in this lot.")
        return redirect(url_for('user.user_dashboard'))

    # Mark spot as occupied
    available_spot.status = 'O'

    # Create reservation
    reservation = Reservation(
        spot_id=available_spot.id,
        user_id=current_user.id,
        start_time=datetime.utcnow()
    )

    db.session.add(reservation)
    db.session.commit()

    flash("Spot reserved successfully.")
    return redirect(url_for('user.user_dashboard'))



# Release a Spot
@user_bp.route('/release/<int:reservation_id>')
@login_required
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != current_user.id:
        flash("Unauthorized action.")
        return redirect(url_for('user.user_dashboard'))

    if reservation.end_time is not None:
        flash("This reservation is already released.")
        return redirect(url_for('user.user_dashboard'))

    # Mark end time
    reservation.end_time = datetime.utcnow()

    # Calculate cost
    lot = reservation.spot.lot
    reservation.calculate_cost(lot.price_per_hour)

    # Free the spot
    reservation.spot.status = 'A'

    db.session.commit()
    flash(f"Spot released. Total cost: ₹{reservation.total_cost}")
    return redirect(url_for('user.user_dashboard'))
