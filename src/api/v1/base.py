from fastapi import APIRouter
import sys
# Объект router, в котором регистрируем обработчики
router = APIRouter()

@router.get('/')
async def root_handler():
    return {'version': 'v1'}

@router.get('/v4')
@router.post('/v4')
async def root_handler2():
    return {'version2': 'v2'}

@router.get('/info')
async def info_handler():
    return {
        'api': 'v1',
        'python': sys.version_info
    }

@router.get('/{action}')
async def action_handler(action):
    return {
        'action': action
    }
