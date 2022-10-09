in vec3 attr_pos;
uniform mat4 modelViewProjection;

out vec3 pos;
out vec3 out_pos;

void main() {
    pos = attr_pos;
    vec4 pos1 = modelViewProjection * vec4(0,0,0,1);
    out_pos = pos1.xyz / pos1.w;
    gl_Position = modelViewProjection * vec4(pos, 1.0);
}
