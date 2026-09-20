#version 330 core
in vec3 vNormal;
in vec3 vWorldPos;

uniform vec3 uLightDir;
uniform vec3 uBaseColor;

out vec4 fragColor;

void main() {
    vec3 N = normalize(vNormal);
    vec3 L = normalize(uLightDir);
    float diff = max(dot(N, L), 0.0);
    vec3 col = uBaseColor * (0.15 + 0.85 * diff);
    fragColor = vec4(col, 1.0);
}
