package top.elfiny;

import android.graphics.Color;
import android.graphics.PixelFormat;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import org.qtproject.qt.android.bindings.QtActivity;

public class GstActivity extends QtActivity {
    private GstPlayer[] players = new GstPlayer[2];

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    public void initPlayers() {
        runOnUiThread(this::initPlayersUi);
    }

    public void initPlayersUi() {
        final FrameLayout root =
                (FrameLayout) findViewById(android.R.id.content).getRootView();
        final LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setBackgroundResource(android.R.color.transparent);
        final FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT);
        root.addView(layout, params);
        final LinearLayout layout2 = new LinearLayout(this);
        layout2.setOrientation(LinearLayout.HORIZONTAL);
        layout2.setBackgroundResource(android.R.color.transparent);
        final LinearLayout.LayoutParams params2 = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 0.9f);
        layout.addView(layout2, params2);
        LinearLayout.LayoutParams viewParams = new LinearLayout.LayoutParams(
                0,  // width = 0, weight controls size
                LinearLayout.LayoutParams.MATCH_PARENT,
                1.0f  // weight = 1
        );
        View view = new View(this);
        view.setBackgroundResource(android.R.color.transparent);
        final LinearLayout.LayoutParams params3 = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 0.1f);
        layout.addView(view, params3);


        final GstSurfaceView[] views = new GstSurfaceView[2];
        for (int i = 0; i < 1; i++) {
            players[i] = new GstPlayer();
            views[i] = new GstSurfaceView(this);
            views[i].setZOrderOnTop(true);
            views[i].getHolder().setFormat(PixelFormat.TRANSLUCENT);
            views[i].setBackgroundColor(Color.TRANSPARENT);
            players[i].setView(views[i]);
            layout2.addView(views[i], viewParams);
        }
    }

    @Override
    public void onDestroy()
    {
        super.onDestroy();
        for (int i = 0; i < 2; i++) {
            if (players[i] != null)
                players[i].close();
        }
    }
}
