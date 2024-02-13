from sqlalchemy import create_engine, text
import os
db_connection= os.environ['DB_CONNECTION']
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
        ), {'val': id})
        job=list(result.mappings())
        if not job:
            return None
        else:
            print(job[0])
            return job[0]
def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query= text("insert into applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) values (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
        conn.execute(query,{
                 'job_id':job_id, 
                 'full_name':data['full_name'],
                 'email':data['email'],
                 'linkedin_url':data['linkedin_url'],
                 'education':data['education'],
                 'work_experience':data['work_experience'],
                 'resume_url':data['resume_url']})
        conn.commit()
def add_job_to_db(title, detail, location, salalry, requirements, responsbilities, currency):
    with engine.connect() as conn:
        conn.execute(text("insert into jobs (title, detail, location, salalry, requirements, responsbilities, currency) values(:title, :detail, :location, :salalry, :requirements, :responsbilities, :currency)"),
                     { 'title':title, 'detail':detail, 'location':location, 'salalry':salalry, 'responsbilities': responsbilities, 'requirements': requirements, 'currency': currency})
        try:
            conn.commit()
            return "success"
        except Exception as e:
            return "error"
