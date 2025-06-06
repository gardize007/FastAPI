import os
import shutil
import uuid
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from db.model import DbAdvertisement, DbImage
from schemas import ImageOrderDisplay, ImageAllDisplay
 
UPLOAD_DIR = "uploaded_images"
 
# add images to advertisement
def add_image(id: int,image: UploadFile, db: Session, current_user_id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} not found')
    if advertisement.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No permission to modify this advertisement')
 
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
    name, ext = os.path.splitext(image.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported image format: {ext}. Allowed formats are: {', '.join(ALLOWED_EXTENSIONS)}"
        )
 
    max_order = (
        db.query(func.max(DbImage.order_id))
        .filter(DbImage.advertisement_id == id)
        .scalar()
    )
    if not max_order:
         max_order=0
   
    MAX_NUMBER=5
    if max_order>=MAX_NUMBER:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is limit of images: {MAX_NUMBER}"
        )      
   
    os.makedirs(UPLOAD_DIR, exist_ok=True)
 
    name, ext = os.path.splitext(image.filename)
    unique_filename = f"{name}_{uuid.uuid4().hex}{ext}"
    image_path = os.path.join(UPLOAD_DIR, unique_filename)
 
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
 
    image_record = DbImage(
        order_id=max_order+1,
        original_name=image.filename,
        image_name=unique_filename,
        image_path=image_path,
        image_type=image.content_type,
        advertisement_id=id
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)
 
    return image_record
 
#show one image related to specific advertisement
def get_one_image(id:int,db:Session):
    image=db.query(DbImage).filter(DbImage.id==id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Image with id {id} not found')
 
    path=f'uploaded_images/{image.image_name}'
    return path
 
 
#show all images related to specific advertisement
def get_all_images(id:int,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} not found')
    all_images =(db.query(DbImage)
                 .filter(DbImage.advertisement_id==id)
                 .order_by(DbImage.order_id.asc())
                 .all())
    if not all_images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Images for advertisement with id {id} are not found')  
   
    for image in all_images:
            image.image_path=f"http://127.0.0.1:8000/images/{image.image_name}"
    return all_images
 
 
#changing order of images related to advertisement
def change_image_order(image_id:int,new_order:int,db:Session,current_user_id:int):
   
    image=db.query(DbImage).filter(DbImage.id==image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} is not found')
   
    advertisement:DbAdvertisement=image.advertisement
    user_id=advertisement.user_id
 
    if user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No permission to modify this advertisement')
   
    if image.order_id==new_order:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='The order is the same')
   
    max_order = (
        db.query(func.max(DbImage.order_id))
        .filter(DbImage.advertisement_id == advertisement.id)
        .scalar()
    )
 
    if new_order<=0 or new_order>max_order:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'The new order_id should be  greater than 0 and less than {max_order}')
   
    repl_image=db.query(DbImage).filter(DbImage.order_id==new_order).first()
    if repl_image:
        repl_image.order_id = image.order_id
 
    image.order_id = new_order
 
    db.commit()
    db.refresh(image)
    if repl_image:
        db.refresh(repl_image)
 
    all_images =(db.query(DbImage)
                 .filter(DbImage.advertisement_id==advertisement.id)
                 .order_by(DbImage.order_id.asc())
                 .all())
   
    for image in all_images:
            image.image_path=f"http://127.0.0.1:8000/images/{image.image_name}"
 
    return all_images
 
 
#delete one image from advertisement
def delete_image(image_id:int,db:Session,current_user_id:int):
 
    image=db.query(DbImage).filter(DbImage.id==image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id {image_id} not found')
   
    advertisement:DbAdvertisement=image.advertisement
    user_id=advertisement.user_id
   
    if user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No permission to modify this advertisement')
   
    image_path = image.image_path  
    full_path = os.path.join(UPLOAD_DIR, os.path.basename(image_path))
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print(f"File {full_path} not found, might already be deleted.")
 
    db.delete(image)
    db.commit()
    return {"message": f"Image with id {image_id} has been deleted"}
 