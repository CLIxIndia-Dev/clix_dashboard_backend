from app import app
from config import Config

# TO get all the relevant credentials for postgresql backend

DB_TYPE = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = Config.POSTGRES_USER
DB_PASS = Config.POSTGRES_PASSWORD
DB_HOST = '172.17.0.1'
DB_PORT = Config.POSTGRES_PORT
DB_NAME = 'clix_dashboard_db'
POOL_SIZE = 50
SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
                                                  DB_PASS, DB_HOST, DB_PORT, DB_NAME)

from sqlalchemy import create_engine, MetaData
#from config.clix_config import SQLALCHEMY_DATABASE_URI, POOL_SIZE

from app.models.user.schema import User
from app.models.school.schema import StateDetails,DistrictDetails,DistrictToSchoolMapping
from app import db
import time
import pandas as pd
import xlrd

Engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=POOL_SIZE, max_overflow=0)
connec = Engine.connect()

def create_state_data():
    '''
    fetch all unique schools in db
    :return: list of schools
    '''
    worksheets = ['CG Schools', 'MZ Schools', 'RJ Schools', 'TS Schools']
    #state_codes = []
    #all_schools = connec.execute('SELECT DISTINCT school_server_code FROM metric1;').fetchall()

    for ws in worksheets:
        df = pd.read_excel('CLIxDashboard-Login-IDs.xlsx', sheet_name=ws, usecols=['State code','StateName'])
        df = df.drop_duplicates(subset=['State code','StateName'])
        print("final dataframe:",df)
        
        for i in df.index:
            statedata = StateDetails(state_code=int(df['State code'].values[0]), stateName=str(df['StateName'].values[0]))

        # adminuser.set_password(password=passwd)
        
            try:
                db.session.add(statedata)
                db.session.commit()
                print('Added state {0} to db.'.format(statedata.state_code))
            except Exception as e:  
                print(e)
                time.sleep(2)


        #return None        
    #print('State codes:', len(state_codes))

    #return state_codes

def create_distirct_data():
    '''
    fetch all unique schools in db
    :return: list of schools
    '''
    worksheets = ['CG Schools', 'MZ Schools', 'RJ Schools', 'TS Schools']
    #state_codes = []
    #all_schools = connec.execute('SELECT DISTINCT school_server_code FROM metric1;').fetchall()

    for ws in worksheets:
        df = pd.read_excel('CLIxDashboard-Login-IDs.xlsx', sheet_name=ws, usecols=['State code','District name', 'District code'])
        df = df.drop_duplicates(subset=['District name']).reset_index()
        print("final dataframe:",df)
        
        for i in df.index:
            #for j in range(0,len(df['state_code'].values))
            distirctdata = DistrictDetails(state_code=int(df['State code'].values[i]), distirct_code=str(df['District code'].values[i]), districtName=str(df['District name'].values[i]))

            try:
                db.session.add(distirctdata)
                db.session.commit()
                print('Added district {0} to db.'.format(distirctdata.districtName))
            except Exception as e:  
                print(e)
                time.sleep(2)
        

def create_school_data():
    '''
    fetch all unique schools in db
    :return: list of schools
    '''
    worksheets = ['CG Schools', 'MZ Schools', 'RJ Schools', 'TS Schools']
    #state_codes = []
    #all_schools = connec.execute('SELECT DISTINCT school_server_code FROM metric1;').fetchall()

    for ws in worksheets:
        df = pd.read_excel('CLIxDashboard-Login-IDs.xlsx', sheet_name=ws, usecols=['State code', 'District code', 'School Name', 'Full CLIx School Code', 'Server id '])
        #df = df.drop_duplicates(subset=['District name']).reset_index()
        #print("final dataframe:",df)
        
        for i in df.index:
            #for j in range(0,len(df['state_code'].values))
            schooldata = DistrictToSchoolMapping(state_code=int(df['State code'].values[i]), distirct_code=str(df['District code'].values[i]), school_name=str(df['School Name'].values[i]), school_server_code=str(df['Full CLIx School Code'].values[i]), server_id=str(df['Server id '].values[i]))
            try:
                db.session.add(schooldata)
                db.session.commit()
                print('Added school {0} to db.'.format(schooldata.school_name))
            except Exception as e:  
                print(e)
                time.sleep(2)

if __name__ == '__main__':
    create_school_data()
    #create_distirct_data()
    #create_state_data()
    #create_school_users(get_all_schools())

