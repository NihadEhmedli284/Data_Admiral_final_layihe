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
        age = request.form.get('age')
        grade = request.form.get('grade')
        free_day = request.form.get('free_day')
        activity = request.form.get('activity')
        companion = request.form.get('companion')
        hours_per_day = request.form.get('hours_per_day')
        satisfaction = request.form.get('satisfaction') or request.form.get('satisfaction_rating')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM activities WHERE name = %s;", (activity,))
        row = cur.fetchone()
        if row:
            activity_id = row[0]
        else:
            cur.execute(
                "INSERT INTO activities (name) VALUES (%s) RETURNING id;",
                (activity,)
            )
            activity_id = cur.fetchone()[0]

        cur.execute("SELECT id FROM companions WHERE name = %s;", (companion,))
        row = cur.fetchone()
        if row:
            companion_id = row[0]
        else:
            cur.execute(
                "INSERT INTO companions (name) VALUES (%s) RETURNING id;",
                (companion,)
            )
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
