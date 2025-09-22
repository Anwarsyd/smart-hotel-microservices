import os

folders = [
    "services/user-service/app/{controllers,models,routes,schemas,services,middleware,utils,database,config}",
    "services/hotel-service/app/{controllers,models,routes,schemas,services,utils,database,config}",
    "services/booking-service/app/{controllers,models,routes,schemas,services,utils,database,config}",
    "services/payment-service/app/{controllers,models,routes,schemas,services,utils,database,config}",
    "services/notification-service/app/{controllers,models,routes,schemas,services,utils,database,config}",
    "services/face-recognition-service/app/{controllers,models,routes,schemas,services,utils,database,ml_models,storage}",
    "services/api-gateway/app/{middleware,routes,services,utils,config}"
]

for path in folders:
    for p in path.split(','):
        os.makedirs(p.replace('{','').replace('}','').strip(), exist_ok=True)
print("Folder structure created!")
