#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

uniform mat4 uMVP;

out vec3 vNormal;
out vec3 vWorldPos;

void main() {
    vNormal = normalize(mat3(uMVP) * aNormal);
    vec4 wp = uMVP * vec4(aPos, 1.0);
    vWorldPos = wp.xyz;
    gl_Position = wp;
}
