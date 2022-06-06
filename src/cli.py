import sentry_sdk
from src.runner import Runner
from src.verify import ExerciseSeeker
from src.constants import exercise_files_architecture
from src.utils.starklings_directory import StarklingsDirectory, VersionManager
from src.solution import SolutionPatcher
from src.config import root_directory

sentry_sdk.init(
    "https://73212d09152344fd8e351ef180b8fa75@o1254095.ingest.sentry.io/6421829",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


def capture_solution_request(solution_path: str):
    with sentry_sdk.push_scope() as scope:
        scope.set_tag("requested_solution", str(solution_path))
        sentry_sdk.capture_message("Solution requested", level="info")


async def cli(args):
    starklings_directory = StarklingsDirectory()
    version_manager = VersionManager(starklings_directory)

    if args.version:
        version_manager.print_current_version()

    if args.watch:
        sentry_sdk.capture_message("Starting the watch mode")
        runner = Runner(root_directory)
        runner.run()

    if args.verify:
        sentry_sdk.capture_message("Verifying all the exercises")
        seeker = ExerciseSeeker(exercise_files_architecture, root_directory)
        exercise_path = seeker.find_next_exercise()

        if not exercise_path:
            print("All exercises finished ! 🎉")
        else:
            print(exercise_path)

    if args.solution:
        capture_solution_request(args.solution)
        displayer = SolutionPatcher(args.solution, root_directory)
        solution = displayer.get_solution()
        if solution:
            print(solution)
        else:
            print("Solution file not found")
