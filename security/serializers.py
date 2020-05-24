from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        user = self.user
        data.update({
            'groups': [user_group.name for user_group in user.groups.all()],
            'authenticated': True,
            'email': user.email
        })
        return data
