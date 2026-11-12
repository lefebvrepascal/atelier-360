import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
W,H=4096,2048
def wall(src,out,hfov,el_c=0):
    im=Image.open(src).convert("RGB"); sw=int(W*hfov/360); sh=int(sw*im.height/im.width)
    a=np.asarray(im.resize((sw,sh),Image.LANCZOS)).astype(np.float32)
    y=np.linspace(0,1,H)[:,None,None]
    bg=np.where(y<0.5, np.array([14,16,22])*(0.6+0.8*y), np.array([20,18,16])*(1.4-0.8*y))
    cv=np.broadcast_to(bg,(H,W,3)).copy()
    yc=int(H/2-el_c/180*H); y0=yc-sh//2; x0=(W-sw)//2
    ex=int(sw*0.035); ey=int(sh*0.08)
    fx=np.clip(np.minimum(np.arange(sw),sw-1-np.arange(sw))/ex,0,1); fy=np.clip(np.minimum(np.arange(sh),sh-1-np.arange(sh))/ey,0,1)
    m=(np.sqrt(fy[:,None]*fx[None,:]))[...,None]
    reg=cv[y0:y0+sh,x0:x0+sw]; cv[y0:y0+sh,x0:x0+sw]=a*m+reg*(1-m)
    # faint reflection below
    r=a[::-1][:int(sh*0.35)]*0.18; rh=r.shape[0]; fr=np.linspace(1,0,rh)[:,None,None]*fx[None,:,None]
    cv[y0+sh+8:y0+sh+8+rh,x0:x0+sw]+=r*fr
    Image.fromarray(np.clip(cv,0,255).astype(np.uint8)).save(out,quality=90)
P="/home/claude/wmed/medias/panos/"
wall(P+"oradour1.jpg","oradour_w.jpg",200)
wall(P+"hiroshima.jpg","hiroshima_w.jpg",180,el_c=2)
wall(P+"arromanches.jpg","arromanches_w.jpg",180)
