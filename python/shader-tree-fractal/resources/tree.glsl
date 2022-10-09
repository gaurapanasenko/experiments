#version 330 core

#if defined VERTEX_SHADER

in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}

#elif defined GEOMETRY_SHADER

layout (lines) in;
layout (triangle_strip, max_vertices = 64) out;

out vec3 pos;
out vec3 normal;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform float m_size;

vec3 CIRCLE[17];

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
    //~ CIRCLE[0] = vec3(0,1,0);
    //~ CIRCLE[1] = vec3(0,0,1);
    //~ CIRCLE[2] = vec3(0,-1,0);
    //~ CIRCLE[3] = vec3(0,0,-1);
    //~ CIRCLE[4] = vec3(0,1,0);
    
    CIRCLE[0] = vec3(0, 1.0, 0.0);
    CIRCLE[1] = vec3(0, 0.9238795325112867, 0.3826834323650898);
    CIRCLE[2] = vec3(0, 0.7071067811865476, 0.7071067811865475);
    CIRCLE[3] = vec3(0, 0.38268343236508984, 0.9238795325112867);
    CIRCLE[4] = vec3(0, 6.123233995736766e-17, 1.0);
    CIRCLE[5] = vec3(0, -0.3826834323650897, 0.9238795325112867);
    CIRCLE[6] = vec3(0, -0.7071067811865475, 0.7071067811865476);
    CIRCLE[7] = vec3(0, -0.9238795325112867, 0.3826834323650899);
    CIRCLE[8] = vec3(0, -1.0, 1.2246467991473532e-16);
    CIRCLE[9] = vec3(0, -0.9238795325112868, -0.38268343236508967);
    CIRCLE[10] = vec3(0, -0.7071067811865477, -0.7071067811865475);
    CIRCLE[11] = vec3(0, -0.38268343236509034, -0.9238795325112865);
    CIRCLE[12] = vec3(0, -1.8369701987210297e-16, -1.0);
    CIRCLE[13] = vec3(0, 0.38268343236509, -0.9238795325112866);
    CIRCLE[14] = vec3(0, 0.7071067811865474, -0.7071067811865477);
    CIRCLE[15] = vec3(0, 0.9238795325112865, -0.3826834323650904);
    CIRCLE[16] = vec3(0, 1.0, 0.0);

    mat4 mv = m_camera * m_model;
    
    vec3 a = gl_in[0].gl_Position.xyz;
    vec3 b = gl_in[1].gl_Position.xyz;

    vec3 up = vec3(0.0, 1.0, 0.0) * m_size;
    vec3 right = vec3(1.0, 0.0, 0.0) * m_size;
    mat3 rot;
    rot[0] = normalize(b - a);
    rot[1] = normalize(cross(rot[0], vec3(rot[0].z, rot[0].x, rot[0].y)));
    rot[2] = normalize(cross(rot[0], rot[1]));
    
    for (int i = 0; i < 16; i++) {
        vec4 da = mv * vec4(a + rot * CIRCLE[i] * m_size, 1.0);
        vec4 db = mv * vec4(a + rot * CIRCLE[i+1] * m_size, 1.0);
        vec4 dc = mv * vec4(b + rot * CIRCLE[i] * m_size, 1.0);
        vec4 dd = mv * vec4(b + rot * CIRCLE[i+1] * m_size, 1.0);
        draw_face(da, db, dc, dd);
    }
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