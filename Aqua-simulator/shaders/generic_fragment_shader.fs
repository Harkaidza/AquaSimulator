#version 330
in vec2 newTexture;
in vec3 normal;
in vec3 fragPos;
in mat3 normalMatrix;

out vec4 outColor;

uniform sampler2D samplerTexture;
uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{
    float specS = 0.5f;
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec3 ambient = 0.1f * lightColor;
    vec3 norm = normalize(normalMatrix * normal);
    vec3 lightDir = normalize(lightPos - fragPos);
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specS * spec * lightColor;
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    outColor = vec4(ambient + diffuse + specular, 1.0) * texture(samplerTexture, newTexture);
}