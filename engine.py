import chess.engine
import os
import chess.polyglot
class Engine():
    def pull_latest_weights(self, month):
        files = []
        for file in os.listdir(f"{os.getcwd()}/../models/{month}/"):
            if file.endswith(".pb.gz"):
                files.append([int(file.split("-")[-1].split(".pb.gz")[0]), file])
        files = sorted(files, reverse=True)[0][1]
        return files
    def play(self, board: chess.Board, month: str):
        try:
            with chess.polyglot.open_reader(f"../lichess_db_standard_rated_{month}.bin") as reader:
                self.move = reader.choice(board).move
            return self.move
        except IndexError:
            self.engine = chess.engine.SimpleEngine.popen_uci(["/opt/homebrew/bin/lc0", f"--weights={os.getcwd()}/../models/{month}/{self.pull_latest_weights(month)}"])
            self.move = self.engine.play(board, chess.engine.Limit(depth=1)).move
            self.engine.quit()
            return self.move