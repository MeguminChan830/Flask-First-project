from sqlalchemy import create_engine, text
import os
db_connection= os.environ['DB_CONNECION']
engine= create_engine(
    db_connection,
    connect_args={
        "ssl":{
            "ssl_ca":"/etc/ssl/cert.pem"
        }
    }
)
def load_jobs_from_db():
    with engine.connect() as conn:
        result= conn.execute(text("select * from jobs"))
        jobs=[]
        for row in result.mappings().all():
            jobs.append(dict(row))
        return jobs
def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(
            "select * from jobs where id=:val",
            val=id
        ))
        if result.rowcount==0:
            return None
        else:
            return dict(list(result)[0])
def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query= text("insert into applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) values (:job_id, :fullname, :email, :linkedin_url, :education, :work_experience, :resume_url)")
        conn.execute(query, 
                 job_id=job_id, 
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])
        conn.commit()

