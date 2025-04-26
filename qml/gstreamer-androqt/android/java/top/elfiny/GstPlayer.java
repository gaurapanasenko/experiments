package top.elfiny;

import android.view.Surface;
import android.view.SurfaceHolder;
import org.jetbrains.annotations.NotNull;

class GstPlayer implements SurfaceHolder.Callback {
    private SurfaceHolder surfaceHolder = null;
    private GstSurfaceView surfaceView = null;

    private native void initJni();
    private native void releaseJni();
    private native void playJni();
    private native void pauseJni();
    private native void surfaceInitJni(Object surface);
    private native void surfaceReleaseJni();

    GstPlayer() {
        initJni();
    }

    public void play() {
        playJni();
    }

    public void pause() {
        pauseJni();
    }

    public void setView(GstSurfaceView surfaceView) {
        if (this.surfaceView == surfaceView)
            return;
        if (this.surfaceView != null) {
            surfaceView.getHolder().removeCallback(this);
            surfaceReleaseJni();
        }
        this.surfaceView = surfaceView;
        surfaceView.getHolder().addCallback(this);
    }

    @Override
    public void surfaceCreated(SurfaceHolder surfaceHolder) {
    }

    @Override
    public void surfaceChanged(@NotNull SurfaceHolder surfaceHolder, int i, int i1, int i2) {
        Surface surface = surfaceHolder.getSurface();
        if (surface.isValid())
            surfaceInitJni(surface);
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder surfaceHolder) {
        surfaceReleaseJni();
    }

    public void onMediaSizeChanged(int width, int height) {
        surfaceView.updateSizes(width, height);
    }

    public void close() {
        releaseJni();
    }
}
