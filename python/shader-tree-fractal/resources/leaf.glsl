#version 330 core

#if defined VERTEX_SHADER

in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}

#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 256) out;

out vec3 pos;
out vec3 normal;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform float m_size;

vec3 CIRCLE[9];

void draw_face(vec4 a, vec4 b, vec4 c, vec4 d) {
    vec3 norm = normalize(cross((b-a).xyz, (c-a).xyz));
    gl_Position = m_proj * a;
    normal = norm;
    pos = a.xyz;
    EmitVertex();
    gl_Position = m_proj * b;
    normal = norm;
    pos = b.xyz;
    EmitVertex();
    gl_Position = m_proj * c;
    normal = norm;
    pos = c.xyz;
    EmitVertex();
    gl_Position = m_proj * d;
    normal = norm;
    pos = d.xyz;
    EmitVertex();
    EndPrimitive();
}

void main() {
    mat4 mv = m_camera * m_model;

    vec4 a = mv * gl_in[0].gl_Position;

    vec4 up = vec4(0.0, 1.0, 0.0,1) * m_size;
    vec4 right = vec4(1.0, 0.0, 0.0,1) * m_size;
    vec4 forwd = vec4(0.0, 0.0, 1.0,1) * m_size;

    draw_face(a+up+forwd+right, a+up+forwd-right, a+up-forwd+right, a+up-forwd-right);
    draw_face(a-up+forwd+right, a-up+forwd-right, a-up-forwd+right, a-up-forwd-right);

    draw_face(a+forwd+up+right, a+forwd+up-right, a+forwd-up+right, a+forwd-up-right);
    draw_face(a-forwd+up+right, a-forwd+up-right, a-forwd-up+right, a-forwd-up-right);

    draw_face(a+right+forwd+up, a+right+forwd-up, a+right-forwd+up, a+right-forwd-up);
    draw_face(a-right+forwd+up, a-right+forwd-up, a-right-forwd+up, a-right-forwd-up);

    /*for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 8; j++) {
            float small = (4.0-i)/4.0;
            float small2 = (4.0-i-1)/4.0;
            float small3 = (5.0-i+1)/5.0;
            vec4 da = mv * vec4(a + CIRCLE[j] * m_size * small - right * i * small3 * 0.4, 1.0);
            vec4 db = mv * vec4(a + CIRCLE[j+1] * m_size * small - right * i * small3 * 0.4, 1.0);
            vec4 dc = mv * vec4(a + CIRCLE[j] * m_size * small2 - right * (i+1) * small3 * 0.4, 1.0);
            vec4 dd = mv * vec4(a + CIRCLE[j+1] * m_size * small2 - right * (i+1) * small3 * 0.4, 1.0);
            draw_face(da, db, dc, dd);
        }
    }
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 8; j++) {
            float small = (4.0-i)/4.0;
            float small2 = (4.0-i-1)/4.0;
            float small3 = (5.0-i+1)/5.0;
            vec4 da = mv * vec4(a + CIRCLE[j] * m_size * small + right * i * small3 * 0.4, 1.0);
            vec4 db = mv * vec4(a + CIRCLE[j+1] * m_size * small + right * i * small3 * 0.4, 1.0);
            vec4 dc = mv * vec4(a + CIRCLE[j] * m_size * small2 + right * (i+1) * small3 * 0.4, 1.0);
            vec4 dd = mv * vec4(a + CIRCLE[j+1] * m_size * small2 + right * (i+1) * small3 * 0.4, 1.0);
            draw_face(da, db, dc, dd);
        }
    }*/
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

in vec3 pos;
in vec3 normal;

void main() {
    float l = dot(normalize(-pos), normalize(normal));
    fragColor = color * (0.25 + abs(l) * 0.75);
}

#endif