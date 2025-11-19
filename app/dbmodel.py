from typing import Optional
import datetime

from sqlalchemy import BigInteger, CHAR, Date, ForeignKeyConstraint, Index, Integer, JSON, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base, Session, aliased

import sqlalchemy as sqla #create_engine, insert, select
import bcrypt


class Base(DeclarativeBase):
    pass


class MILESTONES(Base):
    __tablename__ = 'MILESTONES'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='MILESTONES_pkey'),
        Index('table_6_mpn34fmhvdc97slrob1_index_0', 'ID')
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    milestone_title: Mapped[Optional[str]] = mapped_column(String(255))


class PROJECTSTATUS(Base):
    __tablename__ = 'PROJECT_STATUS'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PROJECT_STATUS_pkey'),
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status_name: Mapped[Optional[str]] = mapped_column(String(255))
    status_icon_url: Mapped[Optional[str]] = mapped_column(String(1023))

    PROJECTS: Mapped[list['PROJECTS']] = relationship('PROJECTS', back_populates='PROJECT_STATUS')


class PROJECTTECHS(Base):
    __tablename__ = 'PROJECT_TECHS'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PROJECT_TECHS_pkey'),
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tech_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tech_color: Mapped[str] = mapped_column(CHAR(7), nullable=False)
    tech_icon_url: Mapped[Optional[str]] = mapped_column(String(1023))

    PROJECT_TECH_STACK: Mapped[list['PROJECTTECHSTACK']] = relationship('PROJECTTECHSTACK', back_populates='PROJECT_TECHS')


class USER(Base):
    __tablename__ = 'USER'
    __table_args__ = (
        PrimaryKeyConstraint('ID', 'user_name', name='USER_pkey'),
        UniqueConstraint('ID', name='user_id_key')
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_desc: Mapped[Optional[str]] = mapped_column(String(1023))
    user_bg_color: Mapped[Optional[str]] = mapped_column(CHAR(7))
    user_fg_color: Mapped[Optional[str]] = mapped_column(CHAR(7))
    user_accent_color: Mapped[Optional[str]] = mapped_column(CHAR(7))

    PROJECTS: Mapped[list['PROJECTS']] = relationship('PROJECTS', back_populates='USER_',lazy="selectin")
    COLLABORATORS: Mapped[list['COLLABORATORS']] = relationship('COLLABORATORS', back_populates='USER_',lazy="selectin")


    def setPassword(self, passwd:str):
        self.password = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        return self.password

    def checkPassword(self,passwd:str):
        # provided_password = "mysecretpassword".encode('utf-8')
        # return bcrypt.checkpw(passwd.encode("utf-8"), self.password)
        if bcrypt.checkpw(passwd.encode('utf-8'), self.password.encode('utf-8')):
            return True
        else:
            return False



    def __repr__(self):
        return f"USER(u_name: {self.user_name}, passwd: {self.password})"


class Cache(Base):
    __tablename__ = 'cache'
    __table_args__ = (
        PrimaryKeyConstraint('key', name='cache_pkey'),
    )

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    expiration: Mapped[int] = mapped_column(Integer, nullable=False)


class CacheLocks(Base):
    __tablename__ = 'cache_locks'
    __table_args__ = (
        PrimaryKeyConstraint('key', name='cache_locks_pkey'),
    )

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    expiration: Mapped[int] = mapped_column(Integer, nullable=False)


class FailedJobs(Base):
    __tablename__ = 'failed_jobs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='failed_jobs_pkey'),
        UniqueConstraint('uuid', name='failed_jobs_uuid_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False)
    connection: Mapped[str] = mapped_column(Text, nullable=False)
    queue: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    exception: Mapped[str] = mapped_column(Text, nullable=False)
    failed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class JobBatches(Base):
    __tablename__ = 'job_batches'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='job_batches_pkey'),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    pending_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_job_ids: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    options: Mapped[Optional[str]] = mapped_column(Text)
    cancelled_at: Mapped[Optional[int]] = mapped_column(Integer)
    finished_at: Mapped[Optional[int]] = mapped_column(Integer)


class Jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='jobs_pkey'),
        Index('jobs_queue_index', 'queue')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    queue: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    available_at: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    reserved_at: Mapped[Optional[int]] = mapped_column(Integer)


class Migrations(Base):
    __tablename__ = 'migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='migrations_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    migration: Mapped[str] = mapped_column(String(255), nullable=False)
    batch: Mapped[int] = mapped_column(Integer, nullable=False)


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sessions_pkey'),
        Index('sessions_last_activity_index', 'last_activity'),
        Index('sessions_user_id_index', 'user_id')
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    last_activity: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)


class PROJECTS(Base):
    __tablename__ = 'PROJECTS'
    __table_args__ = (
        ForeignKeyConstraint(['PROJECT_STATUS_ID'], ['PROJECT_STATUS.ID'], name='PROJECTS_PROJECT_STATUS_ID_fkey'),
        ForeignKeyConstraint(['USER_ID_PM'], ['USER.ID'], name='PROJECTS_USER_ID_PM_fkey'),
        PrimaryKeyConstraint('ID', name='PROJECTS_pkey')
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    USER_ID_PM: Mapped[int] = mapped_column(Integer, nullable=False)
    PROJECT_STATUS_ID: Mapped[int] = mapped_column(Integer, nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_desc: Mapped[Optional[str]] = mapped_column(String(1023))
    project_start: Mapped[Optional[datetime.date]] = mapped_column(Date)
    project_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    project_links: Mapped[Optional[dict]] = mapped_column(JSON)
    project_milestone: Mapped[Optional[dict]] = mapped_column(JSON)

    PROJECT_STATUS: Mapped['PROJECTSTATUS'] = relationship('PROJECTSTATUS', back_populates='PROJECTS')
    USER_: Mapped['USER'] = relationship('USER', back_populates='PROJECTS')
    COLLABORATORS: Mapped[list['COLLABORATORS']] = relationship('COLLABORATORS', back_populates='PROJECTS_')
    PROJECT_TECH_STACK: Mapped[list['PROJECTTECHSTACK']] = relationship('PROJECTTECHSTACK', back_populates='PROJECTS_')


class COLLABORATORS(Base):
    __tablename__ = 'COLLABORATORS'
    __table_args__ = (
        ForeignKeyConstraint(['PROJECTS_ID'], ['PROJECTS.ID'], name='COLLABORATORS_PROJECTS_ID_fkey'),
        ForeignKeyConstraint(['USER_ID'], ['USER.ID'], name='COLLABORATORS_USER_ID_fkey'),
        PrimaryKeyConstraint('ID', name='COLLABORATORS_pkey')
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    USER_ID: Mapped[int] = mapped_column(Integer, nullable=False)
    PROJECTS_ID: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(255))

    PROJECTS_: Mapped['PROJECTS'] = relationship('PROJECTS', back_populates='COLLABORATORS')
    USER_: Mapped['USER'] = relationship('USER', back_populates='COLLABORATORS')


class PROJECTTECHSTACK(Base):
    __tablename__ = 'PROJECT_TECH_STACK'
    __table_args__ = (
        ForeignKeyConstraint(['PROJECTS_ID'], ['PROJECTS.ID'], name='PROJECT_TECH_STACK_PROJECTS_ID_fkey'),
        ForeignKeyConstraint(['TECH_ID'], ['PROJECT_TECHS.ID'], name='PROJECT_TECH_STACK_TECH_ID_fkey'),
        PrimaryKeyConstraint('ID', name='PROJECT_TECH_STACK_pkey')
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TECH_ID: Mapped[Optional[int]] = mapped_column(Integer)
    PROJECTS_ID: Mapped[Optional[int]] = mapped_column(Integer)

    PROJECTS_: Mapped[Optional['PROJECTS']] = relationship('PROJECTS', back_populates='PROJECT_TECH_STACK')
    PROJECT_TECHS: Mapped[Optional['PROJECTTECHS']] = relationship('PROJECTTECHS', back_populates='PROJECT_TECH_STACK')




PG_CONN = "postgresql://neondb_owner:npg_acPDhfweX3b7@ep-aged-cloud-a1hno2fp-pooler.ap-southeast-1.aws.neon.tech/proman?sslmode=require&channel_binding=require"


def getUserDetails(user_name:str):
    engine = sqla.create_engine(PG_CONN)
    with Session(engine) as session:

        stmt = (
            sqla.select(USER)
            .where(USER.user_name == user_name)
        )
        # Raw SQL
        result = session.execute(stmt).scalars().first()
        return result
    


def createNewUser(user_name:str,passwd:str):
    new_user = USER(
        user_name = user_name,
    )
    new_user.setPassword(passwd)
    
    engine = sqla.create_engine(PG_CONN)
    with Session(engine) as session:
        try:
            session.add(new_user)
            # print(a)

        except:
            session.rollback()
            raise
        # stmt = (
        #     sqla.insert(USER)
        # )
        # # Raw SQL
        # result = session.execute(stmt).scalars().first()
        # return result
        session.commit()

        session.refresh(new_user)

    return new_user


# ------------------------------- Project Model ------------------------------ #

def getProject(id:int):
    engine = sqla.create_engine(PG_CONN)

    with Session(engine) as session:
        stmt = (
            sqla.select(PROJECTS)
            .where(PROJECTS.ID == id)
            .options(
                sqla.orm.selectinload(PROJECTS.COLLABORATORS).selectinload(COLLABORATORS.USER_),
                sqla.orm.selectinload(PROJECTS.PROJECT_TECH_STACK).selectinload(PROJECTTECHSTACK.PROJECT_TECHS),
            )
        )

        project = session.execute(stmt).scalars().first()
        return project
    
def getProjectRaw(id:int):
    engine = sqla.create_engine(PG_CONN)

    with engine.connect() as conn:
        rows = conn.execute(sqla.text(f"""
        SELECT
            p.*,
            c."ID" AS collaborator_id,
            c."role" AS collaborator_role,
            u."ID" AS user_id,
            u."user_name" AS user_name
        FROM "{PROJECTS.__tablename__}" p
        LEFT JOIN "{COLLABORATORS.__tablename__}" c ON c."PROJECTS_ID" = p."ID"
        LEFT JOIN "{USER.__tablename__}" u ON u."ID" = c."USER_ID"
        WHERE p."ID" = :id
        
        """), {"id": id}).mappings().first()

    return rows


def createNewProject(data_json:dict):
    engine = sqla.create_engine(PG_CONN)
    with Session(engine) as session:
        try:
            new_project = PROJECTS(
                USER_ID_PM = data_json.get("USER_ID_PM"),
                PROJECT_STATUS_ID = data_json.get("PROJECT_STATUS_ID"),
                project_name = data_json.get("project_name"),
                project_desc = data_json.get("project_desc"),
                project_start = data_json.get("project_start"),
                project_date = data_json.get("project_date"),
                project_links = data_json.get("project_links"),
            )

            session.add(new_project)
            session.flush()
            session.refresh(new_project)

            prj_collab = []
            prj_tech = []

            # if type(data_json.get("collaborators")) != list:
            #     return None
            
            for collab_uname in data_json.get("collaborators",[]):
                user = session.query(USER).filter(
                    USER.user_name.like(collab_uname)
                ).first()

                temp_collab = COLLABORATORS()
                temp_collab.PROJECTS_ID = new_project.ID
                temp_collab.USER_ID = user.ID
                session.add(user)
                prj_collab.append(temp_collab)

        



            if type(data_json.get("technologies")) != list:
                return None
            
            for tech_id in data_json.get("technologies",[]):
                temp_tech = PROJECTTECHSTACK()
                temp_tech.PROJECTS_ID = new_project.ID 
                temp_tech.TECH_ID = tech_id
                session.add(user)
                prj_tech.append(temp_tech)


            new_project.COLLABORATORS = prj_collab
            new_project.PROJECT_TECH_STACK = prj_tech



            engine = sqla.create_engine(PG_CONN)
            
        
            # session.add(new_project)
            session.expunge(new_project)
            session.commit()
            # session.refresh(new_project)
        except Exception:
            session.rollback()
            raise

    # new_project.COLLABORATORS = prj_collab
    # new_project.PROJECT_TECH_STACK = prj_tech
    # print(new_project.project_name)
    return {"success":True}





def main():
    # Create engine
    engine = sqla.create_engine(PG_CONN)

    # Open a session
    with Session(engine) as session:

        stmt = (
            sqla.select(USER)
        )
        # Raw SQL
        result = session.execute(sqla.select(USER)).scalars().all()
        # print(result)
        # Print rows
        for row in result:
            print(row)


    

if __name__ == "__main__":
    # main()
    # getUserDetails("aaa")

    new_project = {
        "USER_ID_PM" : 1,
        "PROJECT_STATUS_ID" : 1,
        "project_name" : "coba dari flask2",
        "project_desc" : "lorem ipsum dolor sit amet",        
        "project_start" : datetime.date(2024, 1, 1),
        "project_date" : datetime.date(2024, 12, 31),
        "project_links" : {"github": "https://github.com/example/coba", "website": "https://coba.com"},
        "project_milestone" : {"milestone1": "completed", "milestone2": "in progress"},
        "collaborators" : ["orang2","orang3"],
        "technologies" : [1,2]
    }    


    # createNewProject(new_project)


    # a = getProject(82)
    b = getProjectRaw(82)
    print(b)


    # # print(a.COLLABORATORS)
    # for i in a.COLLABORATORS:
    #     print(i.USER_.user_name)
    # a = createNewUser("halo","satu")
    # print(a)