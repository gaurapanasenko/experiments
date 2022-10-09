#version 430

#define TRANS_NUM 16

layout (local_size_x = 1, local_size_y = 1) in;
layout(binding=0) buffer layoutName
{
    vec4 in_pos[];
};
layout(binding=1) buffer layoutName2
{
    vec4 out_pos[];
};

uniform mat4 transform;
uniform mat4 trans[TRANS_NUM];
uniform int in_offset;
uniform int out_offset;

void main() {
    int id = int(gl_GlobalInvocationID.x);
    int in_id = 2*id + 2*in_offset;
    int out_id = 2*id*TRANS_NUM + 2*out_offset;
    for (int i = 0; i < TRANS_NUM; i++) {
        out_pos[out_id+2*i] = transform * trans[i] * in_pos[in_id];
        out_pos[out_id+2*i+1] = transform * trans[i] * in_pos[in_id+1];

        out_pos[out_id+2*i].xyz /= out_pos[out_id+2*i].a;
        out_pos[out_id+2*i].a = 1;
        out_pos[out_id+2*i+1].xyz /= out_pos[out_id+2*i+1].a;
        out_pos[out_id+2*i+1].a = 1;
    }
}

