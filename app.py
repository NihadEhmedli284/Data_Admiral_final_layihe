import os
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_umVILGU1h5yj@ep-solitary-violet-baw40ho1-pooler.c-8.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        age = request.form['age']
        grade = request.form['grade']
        free_day = request.form['free_day']
        activity = request.form['activity']
        companion = request.form['companion']
        hours_per_day = request.form['hours_per_day']
        satisfaction = request.form.get('satisfaction') or request.form.get('satisfaction_rating')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO activities (activity_name) VALUES (%s) ON CONFLICT (activity_name) DO NOTHING;",
            (activity,)
        )
        cur.execute("SELECT activity_id FROM activities WHERE activity_name = %s;", (activity,))
        activity_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO companions (companion_type) VALUES (%s) ON CONFLICT (companion_type) DO NOTHING;",
            (companion,)
        )
        cur.execute("SELECT companion_id FROM companions WHERE companion_type = %s;", (companion,))
        companion_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO responses (age, grade, free_day, activity_id, companion_id, hours_per_day, satisfaction)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (age, grade, free_day, activity_id, companion_id, hours_per_day, satisfaction)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/')

    except Exception as e:
        return f"Xəta baş verdi: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
