import QtQuick3D 1.15
import QtQuick3D.Materials 1.15
import QtQuick 2.15

CustomMaterial {
    id: root
    property double holeSize: 1
    property double backSizeCoef: 1
    property double spiralCoef: 0
    hasRefraction: true

    shaderInfo: ShaderInfo {
        version: "330"
        type: "GLSL"
        shaderKey: ShaderInfo.Refraction
    }

    Shader {
        id: vertShader
        stage: Shader.Vertex
        shader: "blackHole.vert"
    }

    Shader {
        id: fragShader
        stage: Shader.Fragment
        shader: "blackHole.frag"
    }

    Buffer {
        id: tempBuffer
        name: "temp_buffer"
        format: Buffer.Unknown
        textureFilterOperation: Buffer.Linear
        textureCoordOperation: Buffer.ClampToEdge
        sizeMultiplier: 1.0
        bufferFlags: Buffer.None // aka frame
    }

    passes: [ Pass {
            shaders: [ vertShader, fragShader ]
            commands: [ BufferBlit {
                    destination: tempBuffer
                }, BufferInput {
                    buffer: tempBuffer
                    param: "refractiveTexture"
                }, Blending {
                    srcBlending: Blending.SrcAlpha
                    destBlending: Blending.OneMinusSrcAlpha
                }
            ]
        }
    ]
}
