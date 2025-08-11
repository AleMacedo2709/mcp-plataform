from fastapi import Depends, HTTPException, Request, status

def get_current_roles(request: Request):
    # Se o middleware de auth preencher request.state.roles, usa; senão, header de teste
    roles = getattr(request.state, 'roles', None)
    if roles is None:
        hdr = request.headers.get('x-role', '')  # ex.: 'admin,editor'
        roles = [x.strip() for x in hdr.split(',') if x.strip()]
    return roles or []

def require_roles(*required: str):
    def _dep(roles=Depends(get_current_roles)):
        if not any(r in roles for r in required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return True
    return _dep


def get_current_user(request: Request):
    # Em dev, vamos pegar do header x-user; em produção, middleware AAD definirá request.state.user
    user = getattr(request.state, 'user', None) or request.headers.get('x-user')
    return user or "unknown@local"

def require_owner_or_roles(*roles):
    def _dep(request: Request, roles_found=Depends(get_current_roles)):
        user = get_current_user(request)
        return user, roles_found
    return _dep
