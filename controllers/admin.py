from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import db, ParkingLot, ParkingSpot, User, Reservation

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return redirect(url_for('auth.login'))

    lots = ParkingLot.query.all()
    users = User.query.all()
    reservations = Reservation.query.all()

    return render_template('admin_dashboard.html', lots=lots, users=users, reservations=reservations)


# Create Parking Lot
@admin_bp.route('/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot():
    if current_user.username != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        pincode = request.form['pincode']
        price = float(request.form['price_per_hour'])
        max_spots = int(request.form['max_spots'])

        lot = ParkingLot(name=name, address=address, pincode=pincode,
                         price_per_hour=price, max_spots=max_spots)
        db.session.add(lot)
        db.session.commit()

        # Auto-generate parking spots
        for i in range(max_spots):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)

        db.session.commit()
        flash("Parking Lot created successfully.")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('create_lot.html')


# Edit Parking Lot 
@admin_bp.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    if current_user.username != 'admin':
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        lot.name = request.form['name']
        lot.address = request.form['address']
        lot.pincode = request.form['pincode']
        lot.price_per_hour = float(request.form['price_per_hour'])
        db.session.commit()
        flash("Parking Lot updated.")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_lot.html', lot=lot)

# Delete Parking Lot (only if all spots are free)
@admin_bp.route('/delete_lot/<int:lot_id>')
@login_required
def delete_lot(lot_id):
    if current_user.username != 'admin':
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

    # Check if any spot is occupied
    if any(spot.status == 'O' for spot in spots):
        flash("Cannot delete. Some spots are still occupied.")
        return redirect(url_for('admin.admin_dashboard'))

    for spot in spots:
        db.session.delete(spot)
    db.session.delete(lot)
    db.session.commit()

    flash("Parking Lot deleted successfully.")
    return redirect(url_for('admin.admin_dashboard'))
