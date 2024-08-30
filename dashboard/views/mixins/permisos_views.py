

class UserGroupContextMixin:
    def get_user_group_context(self):
        user = self.request.user
        return {
            'is_admin_or_collaborator': (
                user.groups.filter(name='Administrador').exists() or
                user.groups.filter(name='Colaborador').exists()
            ),
            'is_assistant': user.groups.filter(name='Asistente').exists(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_group_context())
        return context