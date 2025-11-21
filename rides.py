# rides.py
from typing import List, Dict, Any, Optional
from db import fetchall, fetchone, insert_and_get_id, execute_commit
from utils import gen_tr_id
from datetime import datetime

def post_driver_availability(user_id: int, slot_date: str, start_time: str, end_time: str, seats:int, vehicle_info:str, only_female:int):
    # user supplies slot_date in YYYY-MM-DD
    q = "INSERT INTO driver_availability (user_id, date, start_time, end_time, seats, vehicle_info, slot_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    return execute_commit(q, (user_id, slot_date, start_time, end_time, seats, vehicle_info, f"{start_time}-{end_time}"))

def get_drivers_for_date(slot_date: str, only_female_pref=False) -> List[Dict[str,Any]]:
    if only_female_pref:
        q = """SELECT da.id as avail_id, da.user_id, u.name, u.gender, da.start_time, da.end_time, da.slot_time
               FROM driver_availability da JOIN users u ON da.user_id=u.user_id
               WHERE da.date=%s AND u.gender='Female'"""
        return fetchall(q, (slot_date,))
    q = """SELECT da.id as avail_id, da.user_id, u.name, u.gender, da.start_time, da.end_time, da.slot_time
           FROM driver_availability da JOIN users u ON da.user_id=u.user_id
           WHERE da.date=%s"""
    return fetchall(q, (slot_date,))

def create_booking_and_txn(rider_id: int, driver_id: int, availability_id: int, pickup, dropoff, pax:int, female_only:int, amount: float, rider_upi: str) -> Optional[str]:
    conn_id = insert_and_get_id("INSERT INTO bookings (rider_id, driver_id, availability_id, pickup, dropoff, pax, female_only, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                (rider_id, driver_id, availability_id, pickup, dropoff, pax, female_only, 'Pending'))
    if not conn_id:
        return None
    tr_id = gen_tr_id()
    ok = insert_and_get_id("""INSERT INTO tr_details (ID, Name, UPI_ID, AMT, Date, Status, rider_id, driver_id, amount, rider_upi, driver_received)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                 (tr_id, f"Booking:{conn_id}", rider_upi, amount, datetime.utcnow(), 'Pending', rider_id, driver_id, amount, rider_upi, 0.00))
    return tr_id

def confirm_booking_and_remove_availability(booking_id: int, availability_id: int):
    ok1 = execute_commit("UPDATE bookings SET status='Confirmed' WHERE id=%s", (booking_id,))
    if availability_id:
        execute_commit("DELETE FROM driver_availability WHERE id=%s", (availability_id,))
    return ok1

def get_my_bookings(user_id:int, role:str):
    if role == 'Rider':
        return fetchall("SELECT * FROM bookings WHERE rider_id=%s ORDER BY created_at DESC", (user_id,))
    return fetchall("SELECT * FROM bookings WHERE driver_id=%s ORDER BY created_at DESC", (user_id,))
