from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        user = self.user
        user_groups = [user_group.name for user_group in user.groups.all()]

        extra = ''
        if 'majad_administrador' in user_groups:
            admin = user.administrador
            extra = {
                'departamentos': admin.departamentos,
                'municipios': admin.municipios
            }

        data.update({
            'groups': user_groups,
            'authenticated': True,
            'email': user.email,
            'extra': extra
        })
        return data
