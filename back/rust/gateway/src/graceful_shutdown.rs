use salvo::server::ServerHandle;
use tokio::signal;
use tracing::{info, warn};

pub struct GracefulShutdown;

#[allow(clippy::missing_panics_doc)]
impl GracefulShutdown {
    #[cfg(windows)]
    pub fn listen(handle: ServerHandle) {
        tokio::spawn(async move {
            let ctrl_c = async {
                signal::ctrl_c()
                    .await
                    .expect("failed to install ctrl+c handler");
            };

            let terminate = async {
                signal::windows::ctrl_c()
                    .expect("failed to install signal handler")
                    .recv()
                    .await;
            };

            tokio::select! {
                () = terminate => warn!("terminate signal received"),
                () = ctrl_c => warn!("ctrl+c signal received"),
            };

            info!("Shutting down...");
            handle.stop_graceful(None);
        });
    }

    #[cfg(unix)]
    pub fn listen(handle: ServerHandle) {
        tokio::spawn(async move {
            let terminate = async {
                signal::unix::signal(signal::unix::SignalKind::terminate())
                    .expect("failed to install signal handler")
                    .recv()
                    .await;
            };

            let interrupt = async {
                signal::unix::signal(signal::unix::SignalKind::interrupt())
                    .expect("failed to install signal handler")
                    .recv()
                    .await;
            };

            tokio::select! {
                () = terminate => warn!("terminate signal received"),
                () = interrupt => warn!("interrupt signal received"),
            };

            info!("Shutting down...");
            handle.stop_graceful(None);
        });
    }
}
