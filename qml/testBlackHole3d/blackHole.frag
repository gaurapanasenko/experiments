out vec4 fragColor;

in vec3 pos;
in vec3 out_pos;
uniform sampler2D lightProbe1;
uniform sampler2D refractiveTexture;

/*void main() {
    //fragColor = vec4(pos.x * 0.02, pos.y * 0.02, pos.z * 0.02, 1.0);
    vec2 texSize = vec2(textureSize(refractiveTexture, 0));
    vec2 newUV = (gl_FragCoord.xy) / texSize;
    fragColor = texture(refractiveTexture, newUV.xy);
    //fragColor.x = 0.5;
    fragColor.a = 1;
}*/

varying vec2 v_texCoord;

vec2 u_resolution;
vec2 u_mouse;
float u_mass;

vec2 rotate(vec2 mt, vec2 st, float angle){
        //float cos = cos(angle*(sin(PI*time/10000)+1)/2);
        //float sin = sin(angle*0);
        //float cos = cos(angle);
        //float sin = sin(angle*sin(PI*time/1000)/10);
        float cos = cos(angle*backSizeCoef);
        float sin = sin(angle*spiralCoef);

        float nx = (cos * (st.x - mt.x)) + (sin * (st.y - mt.y)) + mt.x;
        float ny = (cos * (st.y - mt.y)) - (sin * (st.x - mt.x)) + mt.y;
        return vec2(nx, ny);
}

void main() {
    u_resolution = vec2(textureSize(refractiveTexture, 0));
    u_mouse = (out_pos.xy+1)/2 * u_resolution;
    u_mass = 0.01;
    vec2 st = gl_FragCoord.xy / u_resolution;
    vec2 mt = u_mouse / u_resolution;

    float dx = st.x - mt.x;
    float dy = st.y - mt.y;

    float resRatio = u_resolution.x / u_resolution.y;
    dx *= resRatio;

    dx /= holeSize;
    dy /= holeSize;

    float dist = sqrt(dx * dx + dy * dy);
    float pull = u_mass / (dist * dist);
    pull = pull*pull*pull;

    vec3 color = vec3(0.0);

    vec2 r = rotate(mt,st,pull);
    vec4 imgcolor = texture2D(refractiveTexture, r);
    color = vec3(
            (imgcolor.x - (pull * 0.25)),
            (imgcolor.y - (pull * 0.25)),
            (imgcolor.z - (pull * 0.25))
    );


    fragColor = vec4(color,1.);
}
