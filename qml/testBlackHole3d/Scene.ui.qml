import QtQuick3D 1.15
import QtQuick3D.Materials 1.15
import QtQuick 2.15

View3D {
    id: view3D
    width: 1280
    height: 720
    property double myX: 0
    property alias spiralCoef: cubeMaterial.spiralCoef
    property alias backSizeCoef: cubeMaterial.backSizeCoef
    environment: sceneEnvironment
    SceneEnvironment {
        id: sceneEnvironment
        antialiasingMode: SceneEnvironment.MSAA
        antialiasingQuality: SceneEnvironment.High
        probeBrightness: 200
        lightProbe: Texture {
            source: "Background.hdr"
        }
    }

    Node {
        id: scene

        PerspectiveCamera {
            id: camera
            z: 350
        }

        DirectionalLight {

        }

        Model {
            id: plane
            x: -0
            y: -0
            source: "#Rectangle"
            scale.z: 85.95438/2.5
            scale.y: 85.95438/2.5
            scale.x: 85.95438/2.5
            z: -979.27863
            materials: rectMaterial
            DefaultMaterial {
                id: rectMaterial
                diffuseMap: Texture {
                    source: "wp2665214.jpg"
                }
            }
        }
        Node {
            eulerRotation.z: myX
            Model {
                id: cubeModel
                source: "#Sphere"
                //visible: false
                materials: cubeMaterial
                x: 100
                z: 0
                scale.z: 6
                scale.y: 6
                scale.x: 6
                BlackHoleMaterial {
                    id: cubeMaterial
                }
            }
        }

        /*Model {
            source: "#Sphere"
            materials: rectMaterial
            x: myX
            y: -145.154
            z: 0
            scale.z: 1
            scale.y: 1
            scale.x: 1
        }*/
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}D{i:4}D{i:5}D{i:8}
}
##^##*/

