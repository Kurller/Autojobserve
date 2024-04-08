from app.models import Scrape
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#create a method to save new jobs to the database
def save_new_jobs_to_database(new_jobs_df):
    try:
        # Connect to the database
        engine = create_engine('postgresql://postgres:1234@localhost/Fastapi')
        Session = sessionmaker(bind=engine)
        session = Session()

        # Add only the new jobs to the database
        for _, row in new_jobs_df.iterrows():
            # Check if the job already exists in the database
            if not session.query(Scrape).filter_by(
                company_Names=row['company_Names'],
                job_titles=row['job_titles'],
                Location=row['Location']
            ).first():
                # If not, add it to the database
                new_job = Scrape(
                    company_Names=row['company_Names'],
                    job_titles=row['job_titles'],
                    Location=row['Location']
                )
                session.add(new_job)

        # Commit the session
        session.commit()

        # Close the database session
        session.close()
    except Exception as e:
        print(e)