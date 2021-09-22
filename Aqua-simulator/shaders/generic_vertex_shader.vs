#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 textureCoords;
in layout(location = 2) vec3 normalCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 newTexture;
out vec3 normal;
out vec3 fragPos;
out mat3 normalMatrix;

void main()
{
    gl_Position = proj * view * model * vec4(position, 1.0f);
    newTexture = vec2(textureCoords.x, 1 - textureCoords.y);
    fragPos = vec3(model * vec4(position, 1.0f));
    normal = normalCoords;
    normalMatrix = mat3(transpose(inverse(model)));
}