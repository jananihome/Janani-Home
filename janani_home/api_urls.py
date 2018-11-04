from accounts.api.urls import router as accounts_router
from educational_need.api.urls import router as educational_needs_router
from rest_framework import routers

router = routers.DefaultRouter()
router.registry.extend(accounts_router.registry)
router.registry.extend(educational_needs_router.registry)
